# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex/cloud/marketplace/v1/metering/image_product_usage_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from yandex.cloud import validation_pb2 as yandex_dot_cloud_dot_validation__pb2
from yandex.cloud.marketplace.v1.metering import usage_record_pb2 as yandex_dot_cloud_dot_marketplace_dot_v1_dot_metering_dot_usage__record__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yandex/cloud/marketplace/v1/metering/image_product_usage_service.proto',
  package='yandex.cloud.marketplace.v1.metering',
  syntax='proto3',
  serialized_options=b'\n(yandex.cloud.api.marketplace.v1.meteringZQgithub.com/yandex-cloud/go-genproto/yandex/cloud/marketplace/v1/metering;metering',
  serialized_pb=b'\nFyandex/cloud/marketplace/v1/metering/image_product_usage_service.proto\x12$yandex.cloud.marketplace.v1.metering\x1a\x1cgoogle/api/annotations.proto\x1a\x1dyandex/cloud/validation.proto\x1a\x37yandex/cloud/marketplace/v1/metering/usage_record.proto\"\xac\x01\n\x1dWriteImageProductUsageRequest\x12\x15\n\rvalidate_only\x18\x01 \x01(\x08\x12 \n\nproduct_id\x18\x02 \x01(\tB\x0c\xe8\xc7\x31\x01\x8a\xc8\x31\x04<=50\x12R\n\rusage_records\x18\x03 \x03(\x0b\x32\x31.yandex.cloud.marketplace.v1.metering.UsageRecordB\x08\x82\xc8\x31\x04\x31-25\"\xba\x01\n\x1eWriteImageProductUsageResponse\x12K\n\x08\x61\x63\x63\x65pted\x18\x01 \x03(\x0b\x32\x39.yandex.cloud.marketplace.v1.metering.AcceptedUsageRecord\x12K\n\x08rejected\x18\x02 \x03(\x0b\x32\x39.yandex.cloud.marketplace.v1.metering.RejectedUsageRecord2\xec\x01\n\x18ImageProductUsageService\x12\xcf\x01\n\x05Write\x12\x43.yandex.cloud.marketplace.v1.metering.WriteImageProductUsageRequest\x1a\x44.yandex.cloud.marketplace.v1.metering.WriteImageProductUsageResponse\";\x82\xd3\xe4\x93\x02\x35\"0/marketplace/v1/metering/imageProductUsage/write:\x01*B}\n(yandex.cloud.api.marketplace.v1.meteringZQgithub.com/yandex-cloud/go-genproto/yandex/cloud/marketplace/v1/metering;meteringb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,yandex_dot_cloud_dot_validation__pb2.DESCRIPTOR,yandex_dot_cloud_dot_marketplace_dot_v1_dot_metering_dot_usage__record__pb2.DESCRIPTOR,])




_WRITEIMAGEPRODUCTUSAGEREQUEST = _descriptor.Descriptor(
  name='WriteImageProductUsageRequest',
  full_name='yandex.cloud.marketplace.v1.metering.WriteImageProductUsageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='yandex.cloud.marketplace.v1.metering.WriteImageProductUsageRequest.validate_only', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='product_id', full_name='yandex.cloud.marketplace.v1.metering.WriteImageProductUsageRequest.product_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\3071\001\212\3101\004<=50', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='usage_records', full_name='yandex.cloud.marketplace.v1.metering.WriteImageProductUsageRequest.usage_records', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\202\3101\0041-25', file=DESCRIPTOR),
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
  serialized_start=231,
  serialized_end=403,
)


_WRITEIMAGEPRODUCTUSAGERESPONSE = _descriptor.Descriptor(
  name='WriteImageProductUsageResponse',
  full_name='yandex.cloud.marketplace.v1.metering.WriteImageProductUsageResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='accepted', full_name='yandex.cloud.marketplace.v1.metering.WriteImageProductUsageResponse.accepted', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rejected', full_name='yandex.cloud.marketplace.v1.metering.WriteImageProductUsageResponse.rejected', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=406,
  serialized_end=592,
)

_WRITEIMAGEPRODUCTUSAGEREQUEST.fields_by_name['usage_records'].message_type = yandex_dot_cloud_dot_marketplace_dot_v1_dot_metering_dot_usage__record__pb2._USAGERECORD
_WRITEIMAGEPRODUCTUSAGERESPONSE.fields_by_name['accepted'].message_type = yandex_dot_cloud_dot_marketplace_dot_v1_dot_metering_dot_usage__record__pb2._ACCEPTEDUSAGERECORD
_WRITEIMAGEPRODUCTUSAGERESPONSE.fields_by_name['rejected'].message_type = yandex_dot_cloud_dot_marketplace_dot_v1_dot_metering_dot_usage__record__pb2._REJECTEDUSAGERECORD
DESCRIPTOR.message_types_by_name['WriteImageProductUsageRequest'] = _WRITEIMAGEPRODUCTUSAGEREQUEST
DESCRIPTOR.message_types_by_name['WriteImageProductUsageResponse'] = _WRITEIMAGEPRODUCTUSAGERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WriteImageProductUsageRequest = _reflection.GeneratedProtocolMessageType('WriteImageProductUsageRequest', (_message.Message,), {
  'DESCRIPTOR' : _WRITEIMAGEPRODUCTUSAGEREQUEST,
  '__module__' : 'yandex.cloud.marketplace.v1.metering.image_product_usage_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.marketplace.v1.metering.WriteImageProductUsageRequest)
  })
_sym_db.RegisterMessage(WriteImageProductUsageRequest)

WriteImageProductUsageResponse = _reflection.GeneratedProtocolMessageType('WriteImageProductUsageResponse', (_message.Message,), {
  'DESCRIPTOR' : _WRITEIMAGEPRODUCTUSAGERESPONSE,
  '__module__' : 'yandex.cloud.marketplace.v1.metering.image_product_usage_service_pb2'
  # @@protoc_insertion_point(class_scope:yandex.cloud.marketplace.v1.metering.WriteImageProductUsageResponse)
  })
_sym_db.RegisterMessage(WriteImageProductUsageResponse)


DESCRIPTOR._options = None
_WRITEIMAGEPRODUCTUSAGEREQUEST.fields_by_name['product_id']._options = None
_WRITEIMAGEPRODUCTUSAGEREQUEST.fields_by_name['usage_records']._options = None

_IMAGEPRODUCTUSAGESERVICE = _descriptor.ServiceDescriptor(
  name='ImageProductUsageService',
  full_name='yandex.cloud.marketplace.v1.metering.ImageProductUsageService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=595,
  serialized_end=831,
  methods=[
  _descriptor.MethodDescriptor(
    name='Write',
    full_name='yandex.cloud.marketplace.v1.metering.ImageProductUsageService.Write',
    index=0,
    containing_service=None,
    input_type=_WRITEIMAGEPRODUCTUSAGEREQUEST,
    output_type=_WRITEIMAGEPRODUCTUSAGERESPONSE,
    serialized_options=b'\202\323\344\223\0025\"0/marketplace/v1/metering/imageProductUsage/write:\001*',
  ),
])
_sym_db.RegisterServiceDescriptor(_IMAGEPRODUCTUSAGESERVICE)

DESCRIPTOR.services_by_name['ImageProductUsageService'] = _IMAGEPRODUCTUSAGESERVICE

# @@protoc_insertion_point(module_scope)
