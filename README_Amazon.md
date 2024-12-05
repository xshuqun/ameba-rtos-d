# AmebaD Amazon FreeRTOS LTS 202406.xx Support

## Support Details

Supports Amazon FreeRTOS LTS 202406.xx with the following submodule version up to match https://github.com/FreeRTOS/FreeRTOS-LTS/
- coreMQTT                    2.1.1 -> 2.3.1
- coreHTTP                    3.0.0 -> 3.1.1
- corePKCS11                  3.5.0 -> 3.6.1
- coreJSON                    3.2.0 -> 3.3.0
- backoffAlgorithm            1.3.0 -> 1.4.1
- AWS IoT Device Shadow       1.3.0 -> 1.4.1
- AWS IoT Device Defender     1.3.0 -> 1.4.0
- AWS IoT Jobs                1.3.0 -> 1.5.1
- AWS MQTT File Streams       1.1.0 (NEW!)
- coreMQTT-Agent              d3668a6 -> 8314c29

## Setup SDK

First, clone this repository.

	git clone https://github.com/xshuqun/ameba-rtos-d.git

Second, add `ameba-amazon-freertos` into `component/common/application/amazon`

	git clone --recurse-submodules -b FreeRTOS-LTS-202406.xx https://github.com/Ameba-AIoT/ameba-amazon-freertos.git component/common/application/amazon/amazon-freertos

## Building with Amazon

In `platform_opts.h` set `#define CONFIG_EXAMPLE_AMAZON_FREERTOS 1`.

## Building SDK

Navigate to `project_lp` and `make all` this will build the km0 firmware:

	cd ameba-rtos-d/project/realtek_amebaD_va0_example/GCC-RELEASE/project_lp
	make all

Output:
- ameba-rtos-d/project/realtek_amebaD_va0_example/GCC-RELEASE/project_lp/km0_boot_all.bin

Next, navigate to `project_hp` and `make all` to build km4 and the final firmware:

	cd ameba-rtos-d/project/realtek_amebaD_va0_example/GCC-RELEASE/project_hp`
	make all

Output:
- ameba-rtos-d/project/realtek_amebaD_va0_example/GCC-RELEASE/project_hp/km4_boot_all.bin
- ameba-rtos-d/project/realtek_amebaD_va0_example/GCC-RELEASE/project_hp/km0_km4_image2.bin

## Reference

For more details, please visit [ameba-amazon-freertos](https://github.com/Ameba-AIoT/ameba-amazon-freertos)