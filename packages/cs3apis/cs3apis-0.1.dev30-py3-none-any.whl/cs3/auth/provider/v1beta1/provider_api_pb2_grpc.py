# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from cs3.auth.provider.v1beta1 import provider_api_pb2 as cs3_dot_auth_dot_provider_dot_v1beta1_dot_provider__api__pb2


class ProviderAPIStub(object):
  """Auth Provider API

  The Auth Provider API is meant to authenticate a client.

  The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
  NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and
  "OPTIONAL" in this document are to be interpreted as described in
  RFC 2119.

  The following are global requirements that apply to all methods:
  Any method MUST return CODE_OK on a succesful operation.
  Any method MAY return NOT_IMPLEMENTED.
  Any method MAY return INTERNAL.
  Any method MAY return UNKNOWN.
  Any method MAY return UNAUTHENTICATED.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Authenticate = channel.unary_unary(
        '/cs3.auth.provider.v1beta1.ProviderAPI/Authenticate',
        request_serializer=cs3_dot_auth_dot_provider_dot_v1beta1_dot_provider__api__pb2.AuthenticateRequest.SerializeToString,
        response_deserializer=cs3_dot_auth_dot_provider_dot_v1beta1_dot_provider__api__pb2.AuthenticateResponse.FromString,
        )


class ProviderAPIServicer(object):
  """Auth Provider API

  The Auth Provider API is meant to authenticate a client.

  The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
  NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and
  "OPTIONAL" in this document are to be interpreted as described in
  RFC 2119.

  The following are global requirements that apply to all methods:
  Any method MUST return CODE_OK on a succesful operation.
  Any method MAY return NOT_IMPLEMENTED.
  Any method MAY return INTERNAL.
  Any method MAY return UNKNOWN.
  Any method MAY return UNAUTHENTICATED.
  """

  def Authenticate(self, request, context):
    """Authenticate authenticates a client.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProviderAPIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Authenticate': grpc.unary_unary_rpc_method_handler(
          servicer.Authenticate,
          request_deserializer=cs3_dot_auth_dot_provider_dot_v1beta1_dot_provider__api__pb2.AuthenticateRequest.FromString,
          response_serializer=cs3_dot_auth_dot_provider_dot_v1beta1_dot_provider__api__pb2.AuthenticateResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'cs3.auth.provider.v1beta1.ProviderAPI', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
