#include <cstdint>

#include "dl_model_base.hpp"
#include "esp_err.h"
#include "esp_log.h"

static const char *TAG = "MCUNET_TEST";

// Il nome del simbolo deriva dal file incorporato:
// mcunet_int8.espdl → _binary_mcunet_int8_espdl_start
extern const uint8_t mcunet_int8_espdl[]
    asm("_binary_mcunet_int8_espdl_start");

extern "C" void app_main(void)
{
    ESP_LOGI(TAG, "Starting MCUNet ESP-DL self-test");

    dl::Model *model = new dl::Model(
        reinterpret_cast<const char *>(mcunet_int8_espdl),
        fbs::MODEL_LOCATION_IN_FLASH_RODATA
    );

    if (model == nullptr) {
        ESP_LOGE(TAG, "Model allocation failed");
        return;
    }

    ESP_LOGI(TAG, "Model loaded successfully");

    const esp_err_t result = model->test();

    if (result == ESP_OK) {
        ESP_LOGI(TAG, "MCUNet self-test passed");
    } else {
        ESP_LOGE(TAG, "MCUNet self-test failed");
    }

    model->profile_memory();
    model->profile_module(true);

    delete model;

    ESP_LOGI(TAG, "Self-test completed");
}