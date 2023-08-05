# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from cs3.ocm.invite.v1beta1 import invite_api_pb2 as cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2


class InviteAPIStub(object):
  """Invite API

  The Invite API is meant to invite users and groups belonging to other
  sync'n'share systems, so that collaboration of resources can be enabled.

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
    self.GenerateInviteToken = channel.unary_unary(
        '/cs3.ocm.invite.v1beta1.InviteAPI/GenerateInviteToken',
        request_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GenerateInviteTokenRequest.SerializeToString,
        response_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GenerateInviteTokenResponse.FromString,
        )
    self.ForwardInvite = channel.unary_unary(
        '/cs3.ocm.invite.v1beta1.InviteAPI/ForwardInvite',
        request_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.ForwardInviteRequest.SerializeToString,
        response_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.ForwardInviteResponse.FromString,
        )
    self.AcceptInvite = channel.unary_unary(
        '/cs3.ocm.invite.v1beta1.InviteAPI/AcceptInvite',
        request_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.AcceptInviteRequest.SerializeToString,
        response_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.AcceptInviteResponse.FromString,
        )
    self.GetRemoteUser = channel.unary_unary(
        '/cs3.ocm.invite.v1beta1.InviteAPI/GetRemoteUser',
        request_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GetRemoteUserRequest.SerializeToString,
        response_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GetRemoteUserResponse.FromString,
        )


class InviteAPIServicer(object):
  """Invite API

  The Invite API is meant to invite users and groups belonging to other
  sync'n'share systems, so that collaboration of resources can be enabled.

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

  def GenerateInviteToken(self, request, context):
    """Generates a new token for the user with a validity of 24 hours.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ForwardInvite(self, request, context):
    """Forwards a received invite to the sync'n'share system provider.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AcceptInvite(self, request, context):
    """Completes an invitation acceptance.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetRemoteUser(self, request, context):
    """Retrieves details about a remote user who has accepted an invite to share.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_InviteAPIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GenerateInviteToken': grpc.unary_unary_rpc_method_handler(
          servicer.GenerateInviteToken,
          request_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GenerateInviteTokenRequest.FromString,
          response_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GenerateInviteTokenResponse.SerializeToString,
      ),
      'ForwardInvite': grpc.unary_unary_rpc_method_handler(
          servicer.ForwardInvite,
          request_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.ForwardInviteRequest.FromString,
          response_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.ForwardInviteResponse.SerializeToString,
      ),
      'AcceptInvite': grpc.unary_unary_rpc_method_handler(
          servicer.AcceptInvite,
          request_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.AcceptInviteRequest.FromString,
          response_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.AcceptInviteResponse.SerializeToString,
      ),
      'GetRemoteUser': grpc.unary_unary_rpc_method_handler(
          servicer.GetRemoteUser,
          request_deserializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GetRemoteUserRequest.FromString,
          response_serializer=cs3_dot_ocm_dot_invite_dot_v1beta1_dot_invite__api__pb2.GetRemoteUserResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'cs3.ocm.invite.v1beta1.InviteAPI', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
