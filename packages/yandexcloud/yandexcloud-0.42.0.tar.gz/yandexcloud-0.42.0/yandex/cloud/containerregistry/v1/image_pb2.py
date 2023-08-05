# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/containerregistry/v1/image.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from yandex.cloud.containerregistry.v1 import blob_pb2 as yandex_dot_cloud_dot_containerregistry_dot_v1_dot_blob__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/containerregistry/v1/image.proto',
  package='yandex.cloud.containerregistry.v1',
  syntax='proto3',
  serialized_options=b'\n%yandex.cloud.api.containerregistry.v1ZWgithub.com/yandex-cloud/go-genproto/yandex/cloud/containerregistry/v1;containerregistry',
  serialized_pb=b'\n-yandex/cloud/containerregistry/v1/image.proto\x12!yandex.cloud.containerregistry.v1\x1a,yandex/cloud/containerregistry/v1/blob.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xfa\x01\n\x05Image\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x64igest\x18\x03 \x01(\t\x12\x17\n\x0f\x63ompressed_size\x18\x04 \x01(\x03\x12\x37\n\x06\x63onfig\x18\x05 \x01(\x0b\x32\'.yandex.cloud.containerregistry.v1.Blob\x12\x37\n\x06layers\x18\x06 \x03(\x0b\x32\'.yandex.cloud.containerregistry.v1.Blob\x12\x0c\n\x04tags\x18\x07 \x03(\t\x12.\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x80\x01\n%yandex.cloud.api.containerregistry.v1ZWgithub.com/yandex-cloud/go-genproto/yandex/cloud/containerregistry/v1;containerregistryb\x06proto3'
  ,
  dependencies=[yandex_dot_cloud_dot_containerregistry_dot_v1_dot_blob__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_IMAGE = _descriptor.Descriptor(
  name='Image',
  full_name='yandex.cloud.containerregistry.v1.Image',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='yandex.cloud.containerregistry.v1.Image.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='yandex.cloud.containerregistry.v1.Image.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='digest', full_name='yandex.cloud.containerregistry.v1.Image.digest', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='compressed_size', full_name='yandex.cloud.containerregistry.v1.Image.compressed_size', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='yandex.cloud.containerregistry.v1.Image.config', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='layers', full_name='yandex.cloud.containerregistry.v1.Image.layers', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tags', full_name='yandex.cloud.containerregistry.v1.Image.tags', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='yandex.cloud.containerregistry.v1.Image.created_at', index=7,
      number=8, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=164,
  serialized_end=414,
)

_IMAGE.fields_by_name['config'].message_type = yandex_dot_cloud_dot_containerregistry_dot_v1_dot_blob__pb2._BLOB
_IMAGE.fields_by_name['layers'].message_type = yandex_dot_cloud_dot_containerregistry_dot_v1_dot_blob__pb2._BLOB
_IMAGE.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['Image'] = _IMAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Image = _reflection.GeneratedProtocolMessageType('Image', (_message.Message,), {
  'DESCRIPTOR' : _IMAGE,
  '__module__' : 'yandex.cloud.containerregistry.v1.image_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.containerregistry.v1.Image)
  })
_sym_db.RegisterMessage(Image)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
