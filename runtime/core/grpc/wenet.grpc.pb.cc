// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: wenet.proto

#include "wenet.pb.h"
#include "wenet.grpc.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/channel_interface.h>
#include <grpcpp/impl/codegen/client_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/rpc_service_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/sync_stream.h>
namespace wenet {

static const char* ASR_method_names[] = {
  "/wenet.ASR/Recognize",
};

std::unique_ptr< ASR::Stub> ASR::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  (void)options;
  std::unique_ptr< ASR::Stub> stub(new ASR::Stub(channel));
  return stub;
}

ASR::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel)
  : channel_(channel), rpcmethod_Recognize_(ASR_method_names[0], ::grpc::internal::RpcMethod::BIDI_STREAMING, channel)
  {}

::grpc::ClientReaderWriter< ::wenet::Request, ::wenet::Response>* ASR::Stub::RecognizeRaw(::grpc::ClientContext* context) {
  return ::grpc::internal::ClientReaderWriterFactory< ::wenet::Request, ::wenet::Response>::Create(channel_.get(), rpcmethod_Recognize_, context);
}

void ASR::Stub::experimental_async::Recognize(::grpc::ClientContext* context, ::grpc::experimental::ClientBidiReactor< ::wenet::Request,::wenet::Response>* reactor) {
  ::grpc::internal::ClientCallbackReaderWriterFactory< ::wenet::Request,::wenet::Response>::Create(stub_->channel_.get(), stub_->rpcmethod_Recognize_, context, reactor);
}

::grpc::ClientAsyncReaderWriter< ::wenet::Request, ::wenet::Response>* ASR::Stub::AsyncRecognizeRaw(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq, void* tag) {
  return ::grpc::internal::ClientAsyncReaderWriterFactory< ::wenet::Request, ::wenet::Response>::Create(channel_.get(), cq, rpcmethod_Recognize_, context, true, tag);
}

::grpc::ClientAsyncReaderWriter< ::wenet::Request, ::wenet::Response>* ASR::Stub::PrepareAsyncRecognizeRaw(::grpc::ClientContext* context, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncReaderWriterFactory< ::wenet::Request, ::wenet::Response>::Create(channel_.get(), cq, rpcmethod_Recognize_, context, false, nullptr);
}

ASR::Service::Service() {
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      ASR_method_names[0],
      ::grpc::internal::RpcMethod::BIDI_STREAMING,
      new ::grpc::internal::BidiStreamingHandler< ASR::Service, ::wenet::Request, ::wenet::Response>(
          [](ASR::Service* service,
             ::grpc::ServerContext* ctx,
             ::grpc::ServerReaderWriter<::wenet::Response,
             ::wenet::Request>* stream) {
               return service->Recognize(ctx, stream);
             }, this)));
}

ASR::Service::~Service() {
}

::grpc::Status ASR::Service::Recognize(::grpc::ServerContext* context, ::grpc::ServerReaderWriter< ::wenet::Response, ::wenet::Request>* stream) {
  (void) context;
  (void) stream;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


}  // namespace wenet
