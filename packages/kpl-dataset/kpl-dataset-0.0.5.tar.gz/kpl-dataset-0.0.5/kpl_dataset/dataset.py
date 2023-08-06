from os import path
import glob
import os
import kpl_dataset.define_pb2 as define
from kpl_dataset import record
from multiprocessing import RLock
from google.protobuf.text_format import MessageToString, Parse

DEFAULT_DATA_NAME = "root"


class ReadOnlyDataset:
    def __init__(self, data_dir, data_name):
        data_name = data_name or DEFAULT_DATA_NAME
        if not path.isfile(path.join(data_dir, "{}.meta".format(data_name))):
            files = glob.glob("{}/*.data".format(data_dir))
            if len(files) == 0:
                raise Exception("Not found dataset in `{}`".format(os.path.abspath(data_dir)))
            data_name = files[0].split(".")[0]
        self._data_file = os.path.join(data_dir, "{}.data".format(data_name))
        self._index_file = os.path.join(data_dir, "{}.index".format(data_name))
        self._meta_file = os.path.join(data_dir, "{}.meta".format(data_name))
        self._data_open = False
        self._data_handle = None
        self.record_type, self._index = self._read_meta_index()
        self._record_count = len(self._index) - 1
        assert self._record_count >= 0, "Dataset length < 0. please make sure dataset closed after all records written"
        self._cursor = 0
        self._meta_db = MetaDB(os.path.join(data_dir, "{}.prop".format(data_name)))

    def _read_meta_index(self):
        with open(self._index_file, "rb") as fi:
            str = fi.read()
            indexes = define.Index()
            indexes.ParseFromString(str)
        with open(self._meta_file, "r") as fi:
            str = fi.read()
            meta = define.Meta()
            Parse(str, meta)
            decode_meta = record.RecordDefine.decode_meta(meta.record_type)
        return decode_meta, indexes.index

    def _init_data_handle(self):
        self._data_handle = open(self._data_file, "rb")

    def next(self):
        if not self._data_open:
            self._init_data_handle()
            self._data_open = True
        if self._cursor >= self._record_count:
            raise StopIteration
        buffer = self._data_handle.read(self._index[self._cursor + 1] - self._index[self._cursor])
        data = define.FeatureMap()
        data.ParseFromString(buffer)
        self._cursor += 1
        return record.RecordDefine.decode(data, self.record_type)

    def get_meta_db(self):
        return self._meta_db

    def __getitem__(self, idx):
        idx = int(idx)
        if not self._data_open:
            self._init_data_handle()
            self._data_open = True
        start = self._index[idx]
        end = self._index[idx + 1]
        self._data_handle.seek(start, 0)
        buffer = self._data_handle.read(end - start)
        data = define.FeatureMap()
        data.ParseFromString(buffer)
        self._cursor = idx
        return record.RecordDefine.decode(data, self.record_type)

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def __len__(self):
        return self._record_count

    def reset(self):
        self._cursor = 0
        self._data_handle.seek(0)

    def close(self):
        if self._data_open:
            self._data_handle.close()


class WriteOnlyDataset:
    VERSION = 1

    def __init__(self, data_dir, data_name, record_type):
        record.RecordDefine.ROOT = data_dir
        if not os.path.exists("{}/{}".format(data_dir, record._FILE_ROOT)):
            os.makedirs("{}/{}".format(data_dir, record._FILE_ROOT))
        self._data_dir = data_dir
        self._data_name = data_name or DEFAULT_DATA_NAME
        self._record_type = record_type
        self._data_handle = open(os.path.join(self._data_dir, "{}.data".format(self._data_name)), "wb")
        self._index_handle = open(os.path.join(self._data_dir, "{}.index".format(self._data_name)), "wb")
        self._meta_file = os.path.join(self._data_dir, "{}.meta".format(self._data_name))
        self._meta_db = MetaDB(os.path.join(self._data_dir, "{}.prop".format(self._data_name)))
        self._index = define.Index()
        self._index.index.append(0)
        self._last_index = 0
        self._valid_write_meta()

    def _valid_write_meta(self):
        meta = record.RecordDefine.encode_meta(self._record_type, self._data_name, self.VERSION)
        with open(self._meta_file, "w") as fo:
            fo.write(MessageToString(meta))
            fo.close()

    def get_meta_db(self):
        return self._meta_db

    def write(self, value):
        example = record.RecordDefine.encode(value, self._record_type)
        example = example.SerializeToString()
        self._last_index += len(example)
        self._index.index.append(self._last_index)
        self._data_handle.write(example)

    def close(self):
        self._data_handle.close()
        self._index_handle.write(self._index.SerializeToString())
        self._index_handle.close()


class MetaDB:
    def __init__(self, file):
        self.meta = define.Property()
        self.file = file
        self._lock = RLock()
        self._prop = None
        self._init = False

    def put(self, key, value):
        assert isinstance(key, str), "dict key must be string. but get `{}`".format(key)
        prop = self._get_prop()
        if key in prop.map:
            raise Exception("key `{}` already exist".format(key))
        prop.map[key].CopyFrom(self._encode_entrance(value))
        self._write_prop(prop)

    def update(self, key, value):
        prop = self._get_prop()
        if key not in prop.map:
            raise Exception("key `{}` not exist".format(key))
        prop.map[key].CopyFrom(self._encode_entrance(value))
        self._write_prop(prop)

    def delete(self, key):
        prop = self._get_prop()
        if key not in prop.map:
            return
        prop.map.pop(key)
        self._write_prop(prop)

    def get(self, key):
        prop = self._get_prop()
        if key not in prop.map:
            return None
        return self._decode(prop.map[key])

    def keys(self):
        prop = self._get_prop()
        return tuple(prop.map.keys())

    def has(self, key):
        prop = self._get_prop()
        return key in prop.map

    def merge_from(self, other):
        assert isinstance(other, MetaDB), "should be MetaDB object. but get `{}`".format(type(other))
        for k in other.keys():
            if self.has(k):
                self.update(k, other.get(k))
            else:
                self.put(k, other.get(k))

    def _get_prop(self):
        if not self._init:
            if not os.path.exists(self.file):
                return define.Property()
        try:
            self._lock.acquire()
            if self._prop is None:
                with open(self.file, "rb") as fo:
                    buffer = fo.read()
                self._prop = define.Property()
                self._prop.ParseFromString(buffer)
        finally:
            self._lock.release()
        return self._prop

    def _write_prop(self, prop):
        # TODO: add lock file
        try:
            self._lock.acquire()
            self._prop = prop
            serialized = prop.SerializeToString()
            with open(self.file, "wb") as fo:
                fo.write(serialized)
                fo.flush()
        finally:
            self._lock.release()
        self._init = True

    def _decode(self, value):
        if value.flag == define.DynamicType.TypeFlag.string_field:
            return value.string
        elif value.flag == define.DynamicType.TypeFlag.float64_field:
            return value.float64
        elif value.flag == define.DynamicType.TypeFlag.int64_field:
            return value.int64
        elif value.flag == define.DynamicType.TypeFlag.list_field:
            decoded = []
            for v in value.list:
                decoded.append(self._decode(v))
            return decoded
        elif value.flag == define.DynamicType.TypeFlag.map_field:
            decoded = {}
            for k, v in value.map.items():
                decoded[k] = self._decode(v)
            return decoded
        else:
            return None

    def _encode_entrance(self, value):
        dt = define.DynamicType()
        self._encode(value, dt)
        return dt

    def _encode(self, value, dt):
        if isinstance(value, list):
            dt.flag = define.DynamicType.TypeFlag.list_field
            for v in value:
                self._encode(v, dt.list.add())
        elif isinstance(value, dict):
            dt.flag = define.DynamicType.TypeFlag.map_field
            for k, v in value.items():
                assert isinstance(k, str), "dict key must be string. but get `{}`".format(k)
                _dt = define.DynamicType()
                self._encode(v, _dt)
                dt.map[k].CopyFrom(_dt)
        elif isinstance(value, float):
            dt.flag = define.DynamicType.TypeFlag.float64_field
            dt.float64 = value
        elif isinstance(value, int):
            dt.flag = define.DynamicType.TypeFlag.int64_field
            dt.int64 = value
        elif isinstance(value, str):
            dt.flag = define.DynamicType.TypeFlag.string_field
            dt.string = value
        else:
            raise Exception("")

    def __str__(self):
        keys = self.keys()
        ret = ""
        for k in keys:
            ret += ">>> {} = {}\n".format(k, self.get(k))
        return ret
