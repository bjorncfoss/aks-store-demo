# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: mensagem.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'mensagem.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emensagem.proto\"#\n\x0fMensagemRequest\x12\x10\n\x08\x63onteudo\x18\x01 \x01(\t\"$\n\x10MensagemResponse\x12\x10\n\x08resposta\x18\x01 \x01(\t2H\n\x0fMensagemService\x12\x35\n\x0e\x45nviarMensagem\x12\x10.MensagemRequest\x1a\x11.MensagemResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mensagem_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MENSAGEMREQUEST']._serialized_start=18
  _globals['_MENSAGEMREQUEST']._serialized_end=53
  _globals['_MENSAGEMRESPONSE']._serialized_start=55
  _globals['_MENSAGEMRESPONSE']._serialized_end=91
  _globals['_MENSAGEMSERVICE']._serialized_start=93
  _globals['_MENSAGEMSERVICE']._serialized_end=165
# @@protoc_insertion_point(module_scope)