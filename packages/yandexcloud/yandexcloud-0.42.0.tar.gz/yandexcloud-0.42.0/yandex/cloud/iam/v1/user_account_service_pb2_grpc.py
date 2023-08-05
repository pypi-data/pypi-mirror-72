# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from yandex.cloud.iam.v1 import user_account_pb2 as yandex_dot_cloud_dot_iam_dot_v1_dot_user__account__pb2
from yandex.cloud.iam.v1 import user_account_service_pb2 as yandex_dot_cloud_dot_iam_dot_v1_dot_user__account__service__pb2


class UserAccountServiceStub(object):
  """A set of methods for managing user accounts. Currently applicable only for [Yandex.Passport accounts](/docs/iam/concepts/#passport).
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Get = channel.unary_unary(
        '/yandex.cloud.iam.v1.UserAccountService/Get',
        request_serializer=yandex_dot_cloud_dot_iam_dot_v1_dot_user__account__service__pb2.GetUserAccountRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_iam_dot_v1_dot_user__account__pb2.UserAccount.FromString,
        )


class UserAccountServiceServicer(object):
  """A set of methods for managing user accounts. Currently applicable only for [Yandex.Passport accounts](/docs/iam/concepts/#passport).
  """

  def Get(self, request, context):
    """Returns the specified UserAccount resource.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_UserAccountServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Get': grpc.unary_unary_rpc_method_handler(
          servicer.Get,
          request_deserializer=yandex_dot_cloud_dot_iam_dot_v1_dot_user__account__service__pb2.GetUserAccountRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_iam_dot_v1_dot_user__account__pb2.UserAccount.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'yandex.cloud.iam.v1.UserAccountService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
