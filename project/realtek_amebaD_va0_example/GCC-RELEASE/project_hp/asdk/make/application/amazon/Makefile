include $(MAKE_INCLUDE_GEN)

.PHONY: all clean

#*****************************************************************************#
#                               VARIABLES	                              #
#*****************************************************************************#
DIR = $(BASEDIR)/component/common/application/amazon/amazon-freertos
vpath %.c $(DIR)

#*****************************************************************************#
#                               Source FILE LIST                              #
#*****************************************************************************#

##amazon_freertos_LTS - demos
#common
CSRC += $(DIR)/demos/common/http_demo_helpers/http_demo_utils.c
CSRC += $(DIR)/demos/common/mqtt_demo_helpers/mqtt_demo_helpers.c
CSRC += $(DIR)/demos/common/mqtt_subscription_manager/mqtt_subscription_manager.c
CSRC += $(DIR)/demos/common/ota_demo_helpers/ota_application_version.c
CSRC += $(DIR)/demos/common/pkcs11_helpers/pkcs11_helpers.c
CSRC += $(DIR)/demos/dev_mode_key_provisioning/src/aws_dev_mode_key_provisioning.c
#coreHTTP
CSRC += $(DIR)/demos/coreHTTP/http_demo_mutual_auth.c
#coreMQTT
CSRC += $(DIR)/demos/coreMQTT/mqtt_demo_mutual_auth.c
#device_shadow_for_aws
CSRC += $(DIR)/demos/device_shadow_for_aws/shadow_demo_main.c
#device_defender_for_aws
CSRC += $(DIR)/demos/device_defender_for_aws/metrics_collector/lwip/metrics_collector.c
CSRC += $(DIR)/demos/device_defender_for_aws/defender_demo.c
CSRC += $(DIR)/demos/device_defender_for_aws/report_builder.c
#jobs_for_aws
CSRC += $(DIR)/demos/jobs_for_aws/jobs_demo.c
#ota
CSRC += $(DIR)/demos/ota/ota_demo_core_mqtt/ota_demo_core_mqtt.c
#ota w/ mqtt file streams aws
CSRC += $(DIR)/demos/ota/ota_demo_mqtt_streams/ota_demo_mqtt_streams.c
CSRC += $(DIR)/demos/ota/ota_demo_mqtt_streams/ota_event_freertos.c
CSRC += $(DIR)/demos/ota/ota_demo_mqtt_streams/mqtt_agent_task.c
CSRC += $(DIR)/demos/ota/ota_demo_mqtt_streams/mqtt_wrapper.c

###libraries - 3rdparty
#mbedtls
CSRC += $(DIR)/libraries/3rdparty/mbedtls_rtk/net_sockets.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/aes.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/aesni.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/arc4.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/aria.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/asn1parse.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/asn1write.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/base64.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/bignum.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/blowfish.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/camellia.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ccm.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/certs.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/chacha20.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/chachapoly.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/cipher.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/cipher_wrap.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/cmac.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/constant_time.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ctr_drbg.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/debug.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/des.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/dhm.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ecdh.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ecdsa.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ecjpake.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ecp.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ecp_curves.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/entropy.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/entropy_poll.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/error.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/gcm.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/havege.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/hkdf.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/hmac_drbg.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/md.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/md2.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/md4.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/md5.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/memory_buffer_alloc.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/nist_kw.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/oid.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/padlock.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pem.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pk.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pk_wrap.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pkcs11.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pkcs12.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pkcs5.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pkparse.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/pkwrite.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/platform.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/platform_util.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/poly1305.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ripemd160.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/rsa.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/rsa_internal.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/sha1.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/sha256.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/sha512.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_cache.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_ciphersuites.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_cli.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_cookie.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_msg.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_srv.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_ticket.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/ssl_tls.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/threading.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/timing.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/version.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/version_features.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/x509.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/x509_create.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/x509_crl.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/x509_crt.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/x509_csr.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/x509write_crt.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/x509write_csr.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls/library/xtea.c
#jsmn
CSRC += $(DIR)/libraries/3rdparty/jsmn/jsmn.c
#mbedtls_utils
CSRC += $(DIR)/libraries/3rdparty/mbedtls_utils/mbedtls_error.c
CSRC += $(DIR)/libraries/3rdparty/mbedtls_utils/mbedtls_utils.c
#tinycbor
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborencoder.c
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborencoder_close_container_checked.c
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborerrorstrings.c
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborparser.c
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborparser_dup_string.c
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborpretty.c
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborpretty_stdio.c
CSRC += $(DIR)/libraries/3rdparty/tinycbor/src/cborvalidation.c

##common
#mqtt_agent
CSRC += $(DIR)/libraries/common/abstractions/mqtt_agent/freertos_agent_message.c
CSRC += $(DIR)/libraries/common/abstractions/mqtt_agent/freertos_command_pool.c

#transport - secure_sockets
CSRC += $(DIR)/libraries/common/abstractions/transport/secure_sockets/transport_secure_sockets.c

##freertos_plus - standard
#crypto
CSRC += $(DIR)/libraries/common/freertos_plus/standard/crypto/src/iot_crypto.c
#tls
CSRC += $(DIR)/libraries/common/freertos_plus/standard/tls/src/iot_tls.c

##logging
CSRC += $(DIR)/libraries/common/logging/iot_logging.c
CSRC += $(DIR)/libraries/common/logging/iot_logging_task_dynamic_buffers.c


##backoffAlgorithm
CSRC += $(DIR)/libraries/backoffAlgorithm/source/backoff_algorithm.c

##coreHTTP + llhttp
CSRC += $(DIR)/libraries/coreHTTP/source/dependency/3rdparty/llhttp/src/api.c
CSRC += $(DIR)/libraries/coreHTTP/source/dependency/3rdparty/llhttp/src/http.c
CSRC += $(DIR)/libraries/coreHTTP/source/dependency/3rdparty/llhttp/src/llhttp.c
CSRC += $(DIR)/libraries/coreHTTP/source/core_http_client.c

##coreJSON
CSRC += $(DIR)/libraries/coreJSON/source/core_json.c

##coreMQTT
CSRC += $(DIR)/libraries/coreMQTT/source/core_mqtt.c
CSRC += $(DIR)/libraries/coreMQTT/source/core_mqtt_serializer.c
CSRC += $(DIR)/libraries/coreMQTT/source/core_mqtt_state.c

##coreMQTT-Agent
CSRC += $(DIR)/libraries/coreMQTT-Agent/source/core_mqtt_agent.c
CSRC += $(DIR)/libraries/coreMQTT-Agent/source/core_mqtt_agent_command_functions.c

##corePKCS11
CSRC += $(DIR)/libraries/corePKCS11/source/portable/mbedtls/core_pkcs11_mbedtls.c
CSRC += $(DIR)/libraries/corePKCS11/source/core_pkcs11.c
CSRC += $(DIR)/libraries/corePKCS11/source/core_pki_utils.c

##device_defender_for_aws
CSRC += $(DIR)/libraries/device_defender_for_aws/source/defender.c

##device_shadow_for_aws
CSRC += $(DIR)/libraries/device_shadow_for_aws/source/shadow.c

##jobs_for_aws
CSRC += $(DIR)/libraries/jobs_for_aws/source/jobs.c
CSRC += $(DIR)/libraries/jobs_for_aws/source/otaJobParser/job_parser.c
CSRC += $(DIR)/libraries/jobs_for_aws/source/otaJobParser/ota_job_handler.c

##ota_for_aws
CSRC += $(DIR)/libraries/ota_for_aws/source/portable/os/ota_os_freertos.c
CSRC += $(DIR)/libraries/ota_for_aws/source/ota.c
CSRC += $(DIR)/libraries/ota_for_aws/source/ota_base64.c
CSRC += $(DIR)/libraries/ota_for_aws/source/ota_cbor.c
CSRC += $(DIR)/libraries/ota_for_aws/source/ota_http.c
CSRC += $(DIR)/libraries/ota_for_aws/source/ota_interface.c
CSRC += $(DIR)/libraries/ota_for_aws/source/ota_mqtt.c

##mqtt_file_streams_for_aws
CSRC += $(DIR)/libraries/mqtt_file_streams_for_aws/source/MQTTFileDownloader.c
CSRC += $(DIR)/libraries/mqtt_file_streams_for_aws/source/MQTTFileDownloader_cbor.c
CSRC += $(DIR)/libraries/mqtt_file_streams_for_aws/source/MQTTFileDownloader_base64.c

#ports
CSRC += $(DIR)/ports/amebaD/aws_main.c
CSRC += $(DIR)/ports/amebaD/ota/ota_pal.c
CSRC += $(DIR)/ports/amebaD/ota/ota_pal_streams.c
CSRC += $(DIR)/ports/amebaD/ota/aws_ota_rtl8721d.c
CSRC += $(DIR)/ports/amebaD/ota/aws_ota_streams_rtl8721d.c
CSRC += $(DIR)/ports/amebaD/pkcs11/core_pkcs11_pal.c
CSRC += $(DIR)/ports/amebaD/secure_sockets/iot_secure_sockets.c
CSRC += $(DIR)/ports/amebaD/wifi/iot_wifi.c

#*****************************************************************************#
#                               Object FILE LIST                              #
#*****************************************************************************#
OBJS =  $(CSRC:.c=.o)

#*****************************************************************************#
#                               Include Dependency                            #
#*****************************************************************************#
-include $(OBJS:.o=.d)

#*****************************************************************************#
#                        RULES TO GENERATE TARGETS                            #
#*****************************************************************************#
all: CORE_TARGETS COPY_RAM_OBJS

#*****************************************************************************#
#              GENERATE OBJECT FILE
#*****************************************************************************#
CORE_TARGETS: $(OBJS)

#*****************************************************************************#
#              CLEAN GENERATED FILES                                          #
#*****************************************************************************#
clean: CLEAN_OBJS
	$(REMOVE) *.o
	$(REMOVE) *.i
	$(REMOVE) *.s
	$(REMOVE) *.d
	$(REMOVE) *.c

-include $(DEPS)	
