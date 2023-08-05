# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/mdb/redis/v1alpha/cluster.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from yandex.cloud.mdb.redis.v1alpha.config import redis5_0_pb2 as yandex_dot_cloud_dot_mdb_dot_redis_dot_v1alpha_dot_config_dot_redis5__0__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/mdb/redis/v1alpha/cluster.proto',
  package='yandex.cloud.mdb.redis.v1alpha',
  syntax='proto3',
  serialized_options=b'\n\"yandex.cloud.api.mdb.redis.v1alphaZHgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/redis/v1alpha;redis',
  serialized_pb=b'\n,yandex/cloud/mdb/redis/v1alpha/cluster.proto\x12\x1eyandex.cloud.mdb.redis.v1alpha\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x34yandex/cloud/mdb/redis/v1alpha/config/redis5_0.proto\"\xd3\x06\n\x07\x43luster\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tfolder_id\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x43\n\x06labels\x18\x06 \x03(\x0b\x32\x33.yandex.cloud.mdb.redis.v1alpha.Cluster.LabelsEntry\x12H\n\x0b\x65nvironment\x18\x07 \x01(\x0e\x32\x33.yandex.cloud.mdb.redis.v1alpha.Cluster.Environment\x12>\n\nmonitoring\x18\x08 \x03(\x0b\x32*.yandex.cloud.mdb.redis.v1alpha.Monitoring\x12=\n\x06\x63onfig\x18\t \x01(\x0b\x32-.yandex.cloud.mdb.redis.v1alpha.ClusterConfig\x12\x12\n\nnetwork_id\x18\n \x01(\t\x12>\n\x06health\x18\x0b \x01(\x0e\x32..yandex.cloud.mdb.redis.v1alpha.Cluster.Health\x12>\n\x06status\x18\x0c \x01(\x0e\x32..yandex.cloud.mdb.redis.v1alpha.Cluster.Status\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"I\n\x0b\x45nvironment\x12\x1b\n\x17\x45NVIRONMENT_UNSPECIFIED\x10\x00\x12\x0e\n\nPRODUCTION\x10\x01\x12\r\n\tPRESTABLE\x10\x02\"?\n\x06Health\x12\x12\n\x0eHEALTH_UNKNOWN\x10\x00\x12\t\n\x05\x41LIVE\x10\x01\x12\x08\n\x04\x44\x45\x41\x44\x10\x02\x12\x0c\n\x08\x44\x45GRADED\x10\x03\"y\n\x06Status\x12\x12\n\x0eSTATUS_UNKNOWN\x10\x00\x12\x0c\n\x08\x43REATING\x10\x01\x12\x0b\n\x07RUNNING\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x0c\n\x08UPDATING\x10\x04\x12\x0c\n\x08STOPPING\x10\x05\x12\x0b\n\x07STOPPED\x10\x06\x12\x0c\n\x08STARTING\x10\x07\"=\n\nMonitoring\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0c\n\x04link\x18\x03 \x01(\t\"\xc4\x01\n\rClusterConfig\x12\x0f\n\x07version\x18\x01 \x01(\t\x12T\n\x10redis_config_5_0\x18\x02 \x01(\x0b\x32\x38.yandex.cloud.mdb.redis.v1alpha.config.RedisConfigSet5_0H\x00\x12<\n\tresources\x18\x03 \x01(\x0b\x32).yandex.cloud.mdb.redis.v1alpha.ResourcesB\x0e\n\x0credis_config\"\xaf\x03\n\x04Host\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\ncluster_id\x18\x02 \x01(\t\x12\x0f\n\x07zone_id\x18\x03 \x01(\t\x12\x11\n\tsubnet_id\x18\x04 \x01(\t\x12<\n\tresources\x18\x05 \x01(\x0b\x32).yandex.cloud.mdb.redis.v1alpha.Resources\x12\x37\n\x04role\x18\x06 \x01(\x0e\x32).yandex.cloud.mdb.redis.v1alpha.Host.Role\x12;\n\x06health\x18\x07 \x01(\x0e\x32+.yandex.cloud.mdb.redis.v1alpha.Host.Health\x12\x39\n\x08services\x18\x08 \x03(\x0b\x32\'.yandex.cloud.mdb.redis.v1alpha.Service\"1\n\x04Role\x12\x10\n\x0cROLE_UNKNOWN\x10\x00\x12\n\n\x06MASTER\x10\x01\x12\x0b\n\x07REPLICA\x10\x02\"?\n\x06Health\x12\x12\n\x0eHEALTH_UNKNOWN\x10\x00\x12\t\n\x05\x41LIVE\x10\x01\x12\x08\n\x04\x44\x45\x41\x44\x10\x02\x12\x0c\n\x08\x44\x45GRADED\x10\x03\"\xef\x01\n\x07Service\x12:\n\x04type\x18\x01 \x01(\x0e\x32,.yandex.cloud.mdb.redis.v1alpha.Service.Type\x12>\n\x06health\x18\x02 \x01(\x0e\x32..yandex.cloud.mdb.redis.v1alpha.Service.Health\"5\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\t\n\x05REDIS\x10\x01\x12\x0c\n\x08SENTINEL\x10\x02\"1\n\x06Health\x12\x12\n\x0eHEALTH_UNKNOWN\x10\x00\x12\t\n\x05\x41LIVE\x10\x01\x12\x08\n\x04\x44\x45\x41\x44\x10\x02\":\n\tResources\x12\x1a\n\x12resource_preset_id\x18\x01 \x01(\t\x12\x11\n\tdisk_size\x18\x02 \x01(\x03\x42n\n\"yandex.cloud.api.mdb.redis.v1alphaZHgithub.com/yandex-cloud/go-genproto/yandex/cloud/mdb/redis/v1alpha;redisb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,yandex_dot_cloud_dot_mdb_dot_redis_dot_v1alpha_dot_config_dot_redis5__0__pb2.DESCRIPTOR,])



_CLUSTER_ENVIRONMENT = _descriptor.EnumDescriptor(
  name='Environment',
  full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.Environment',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ENVIRONMENT_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRODUCTION', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRESTABLE', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=758,
  serialized_end=831,
)
_sym_db.RegisterEnumDescriptor(_CLUSTER_ENVIRONMENT)

_CLUSTER_HEALTH = _descriptor.EnumDescriptor(
  name='Health',
  full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.Health',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HEALTH_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALIVE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEAD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEGRADED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=833,
  serialized_end=896,
)
_sym_db.RegisterEnumDescriptor(_CLUSTER_HEALTH)

_CLUSTER_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATUS_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CREATING', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RUNNING', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPDATING', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOPPING', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOPPED', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STARTING', index=7, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=898,
  serialized_end=1019,
)
_sym_db.RegisterEnumDescriptor(_CLUSTER_STATUS)

_HOST_ROLE = _descriptor.EnumDescriptor(
  name='Role',
  full_name='yandex.cloud.mdb.redis.v1alpha.Host.Role',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ROLE_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MASTER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REPLICA', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1601,
  serialized_end=1650,
)
_sym_db.RegisterEnumDescriptor(_HOST_ROLE)

_HOST_HEALTH = _descriptor.EnumDescriptor(
  name='Health',
  full_name='yandex.cloud.mdb.redis.v1alpha.Host.Health',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HEALTH_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALIVE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEAD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEGRADED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=833,
  serialized_end=896,
)
_sym_db.RegisterEnumDescriptor(_HOST_HEALTH)

_SERVICE_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='yandex.cloud.mdb.redis.v1alpha.Service.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TYPE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REDIS', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SENTINEL', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1853,
  serialized_end=1906,
)
_sym_db.RegisterEnumDescriptor(_SERVICE_TYPE)

_SERVICE_HEALTH = _descriptor.EnumDescriptor(
  name='Health',
  full_name='yandex.cloud.mdb.redis.v1alpha.Service.Health',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HEALTH_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALIVE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEAD', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=833,
  serialized_end=882,
)
_sym_db.RegisterEnumDescriptor(_SERVICE_HEALTH)


_CLUSTER_LABELSENTRY = _descriptor.Descriptor(
  name='LabelsEntry',
  full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.LabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.LabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.LabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=711,
  serialized_end=756,
)

_CLUSTER = _descriptor.Descriptor(
  name='Cluster',
  full_name='yandex.cloud.mdb.redis.v1alpha.Cluster',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='folder_id', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.folder_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.created_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='labels', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.labels', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='environment', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.environment', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='monitoring', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.monitoring', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.config', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='network_id', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.network_id', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='health', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.health', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='yandex.cloud.mdb.redis.v1alpha.Cluster.status', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CLUSTER_LABELSENTRY, ],
  enum_types=[
    _CLUSTER_ENVIRONMENT,
    _CLUSTER_HEALTH,
    _CLUSTER_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=168,
  serialized_end=1019,
)


_MONITORING = _descriptor.Descriptor(
  name='Monitoring',
  full_name='yandex.cloud.mdb.redis.v1alpha.Monitoring',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.mdb.redis.v1alpha.Monitoring.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='yandex.cloud.mdb.redis.v1alpha.Monitoring.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='link', full_name='yandex.cloud.mdb.redis.v1alpha.Monitoring.link', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1021,
  serialized_end=1082,
)


_CLUSTERCONFIG = _descriptor.Descriptor(
  name='ClusterConfig',
  full_name='yandex.cloud.mdb.redis.v1alpha.ClusterConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='yandex.cloud.mdb.redis.v1alpha.ClusterConfig.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='redis_config_5_0', full_name='yandex.cloud.mdb.redis.v1alpha.ClusterConfig.redis_config_5_0', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resources', full_name='yandex.cloud.mdb.redis.v1alpha.ClusterConfig.resources', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='redis_config', full_name='yandex.cloud.mdb.redis.v1alpha.ClusterConfig.redis_config',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1085,
  serialized_end=1281,
)


_HOST = _descriptor.Descriptor(
  name='Host',
  full_name='yandex.cloud.mdb.redis.v1alpha.Host',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.mdb.redis.v1alpha.Host.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cluster_id', full_name='yandex.cloud.mdb.redis.v1alpha.Host.cluster_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zone_id', full_name='yandex.cloud.mdb.redis.v1alpha.Host.zone_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='subnet_id', full_name='yandex.cloud.mdb.redis.v1alpha.Host.subnet_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resources', full_name='yandex.cloud.mdb.redis.v1alpha.Host.resources', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='role', full_name='yandex.cloud.mdb.redis.v1alpha.Host.role', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='health', full_name='yandex.cloud.mdb.redis.v1alpha.Host.health', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='services', full_name='yandex.cloud.mdb.redis.v1alpha.Host.services', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HOST_ROLE,
    _HOST_HEALTH,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1284,
  serialized_end=1715,
)


_SERVICE = _descriptor.Descriptor(
  name='Service',
  full_name='yandex.cloud.mdb.redis.v1alpha.Service',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='yandex.cloud.mdb.redis.v1alpha.Service.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='health', full_name='yandex.cloud.mdb.redis.v1alpha.Service.health', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SERVICE_TYPE,
    _SERVICE_HEALTH,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1718,
  serialized_end=1957,
)


_RESOURCES = _descriptor.Descriptor(
  name='Resources',
  full_name='yandex.cloud.mdb.redis.v1alpha.Resources',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_preset_id', full_name='yandex.cloud.mdb.redis.v1alpha.Resources.resource_preset_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_size', full_name='yandex.cloud.mdb.redis.v1alpha.Resources.disk_size', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1959,
  serialized_end=2017,
)

_CLUSTER_LABELSENTRY.containing_type = _CLUSTER
_CLUSTER.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CLUSTER.fields_by_name['labels'].message_type = _CLUSTER_LABELSENTRY
_CLUSTER.fields_by_name['environment'].enum_type = _CLUSTER_ENVIRONMENT
_CLUSTER.fields_by_name['monitoring'].message_type = _MONITORING
_CLUSTER.fields_by_name['config'].message_type = _CLUSTERCONFIG
_CLUSTER.fields_by_name['health'].enum_type = _CLUSTER_HEALTH
_CLUSTER.fields_by_name['status'].enum_type = _CLUSTER_STATUS
_CLUSTER_ENVIRONMENT.containing_type = _CLUSTER
_CLUSTER_HEALTH.containing_type = _CLUSTER
_CLUSTER_STATUS.containing_type = _CLUSTER
_CLUSTERCONFIG.fields_by_name['redis_config_5_0'].message_type = yandex_dot_cloud_dot_mdb_dot_redis_dot_v1alpha_dot_config_dot_redis5__0__pb2._REDISCONFIGSET5_0
_CLUSTERCONFIG.fields_by_name['resources'].message_type = _RESOURCES
_CLUSTERCONFIG.oneofs_by_name['redis_config'].fields.append(
  _CLUSTERCONFIG.fields_by_name['redis_config_5_0'])
_CLUSTERCONFIG.fields_by_name['redis_config_5_0'].containing_oneof = _CLUSTERCONFIG.oneofs_by_name['redis_config']
_HOST.fields_by_name['resources'].message_type = _RESOURCES
_HOST.fields_by_name['role'].enum_type = _HOST_ROLE
_HOST.fields_by_name['health'].enum_type = _HOST_HEALTH
_HOST.fields_by_name['services'].message_type = _SERVICE
_HOST_ROLE.containing_type = _HOST
_HOST_HEALTH.containing_type = _HOST
_SERVICE.fields_by_name['type'].enum_type = _SERVICE_TYPE
_SERVICE.fields_by_name['health'].enum_type = _SERVICE_HEALTH
_SERVICE_TYPE.containing_type = _SERVICE
_SERVICE_HEALTH.containing_type = _SERVICE
DESCRIPTOR.message_types_by_name['Cluster'] = _CLUSTER
DESCRIPTOR.message_types_by_name['Monitoring'] = _MONITORING
DESCRIPTOR.message_types_by_name['ClusterConfig'] = _CLUSTERCONFIG
DESCRIPTOR.message_types_by_name['Host'] = _HOST
DESCRIPTOR.message_types_by_name['Service'] = _SERVICE
DESCRIPTOR.message_types_by_name['Resources'] = _RESOURCES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Cluster = _reflection.GeneratedProtocolMessageType('Cluster', (_message.Message,), {

  'LabelsEntry' : _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), {
    'DESCRIPTOR' : _CLUSTER_LABELSENTRY,
    '__module__' : 'yandex.cloud.mdb.redis.v1alpha.cluster_pb2'
    # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.redis.v1alpha.Cluster.LabelsEntry)
    })
  ,
  'DESCRIPTOR' : _CLUSTER,
  '__module__' : 'yandex.cloud.mdb.redis.v1alpha.cluster_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.redis.v1alpha.Cluster)
  })
_sym_db.RegisterMessage(Cluster)
_sym_db.RegisterMessage(Cluster.LabelsEntry)

Monitoring = _reflection.GeneratedProtocolMessageType('Monitoring', (_message.Message,), {
  'DESCRIPTOR' : _MONITORING,
  '__module__' : 'yandex.cloud.mdb.redis.v1alpha.cluster_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.redis.v1alpha.Monitoring)
  })
_sym_db.RegisterMessage(Monitoring)

ClusterConfig = _reflection.GeneratedProtocolMessageType('ClusterConfig', (_message.Message,), {
  'DESCRIPTOR' : _CLUSTERCONFIG,
  '__module__' : 'yandex.cloud.mdb.redis.v1alpha.cluster_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.redis.v1alpha.ClusterConfig)
  })
_sym_db.RegisterMessage(ClusterConfig)

Host = _reflection.GeneratedProtocolMessageType('Host', (_message.Message,), {
  'DESCRIPTOR' : _HOST,
  '__module__' : 'yandex.cloud.mdb.redis.v1alpha.cluster_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.redis.v1alpha.Host)
  })
_sym_db.RegisterMessage(Host)

Service = _reflection.GeneratedProtocolMessageType('Service', (_message.Message,), {
  'DESCRIPTOR' : _SERVICE,
  '__module__' : 'yandex.cloud.mdb.redis.v1alpha.cluster_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.redis.v1alpha.Service)
  })
_sym_db.RegisterMessage(Service)

Resources = _reflection.GeneratedProtocolMessageType('Resources', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCES,
  '__module__' : 'yandex.cloud.mdb.redis.v1alpha.cluster_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.mdb.redis.v1alpha.Resources)
  })
_sym_db.RegisterMessage(Resources)


DESCRIPTOR._options = None
_CLUSTER_LABELSENTRY._options = None
# @@protoc_insertion_point(module_scope)
