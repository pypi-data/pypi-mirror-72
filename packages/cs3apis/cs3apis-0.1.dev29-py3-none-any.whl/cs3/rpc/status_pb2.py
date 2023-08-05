# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cs3/rpc/status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cs3.rpc import code_pb2 as cs3_dot_rpc_dot_code__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cs3/rpc/status.proto',
  package='cs3.rpc',
  syntax='proto3',
  serialized_options=_b('\n\013com.cs3.rpcB\013StatusProtoP\001Z\005rpcpb\242\002\007CBOXRPC\312\002\007CS3\\RPC'),
  serialized_pb=_b('\n\x14\x63s3/rpc/status.proto\x12\x07\x63s3.rpc\x1a\x12\x63s3/rpc/code.proto\"Y\n\x06Status\x12\x1b\n\x04\x63ode\x18\x01 \x01(\x0e\x32\r.cs3.rpc.Code\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\r\n\x05trace\x18\x03 \x01(\t\x12\x12\n\ntarget_uri\x18\x04 \x01(\tB7\n\x0b\x63om.cs3.rpcB\x0bStatusProtoP\x01Z\x05rpcpb\xa2\x02\x07\x43\x42OXRPC\xca\x02\x07\x43S3\\RPCb\x06proto3')
  ,
  dependencies=[cs3_dot_rpc_dot_code__pb2.DESCRIPTOR,])




_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='cs3.rpc.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='cs3.rpc.Status.code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='cs3.rpc.Status.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trace', full_name='cs3.rpc.Status.trace', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target_uri', full_name='cs3.rpc.Status.target_uri', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=53,
  serialized_end=142,
)

_STATUS.fields_by_name['code'].enum_type = cs3_dot_rpc_dot_code__pb2._CODE
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'cs3.rpc.status_pb2'
  # @@protoc_insertion_point(class_scope:cs3.rpc.Status)
  })
_sym_db.RegisterMessage(Status)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
