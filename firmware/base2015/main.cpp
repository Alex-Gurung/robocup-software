#include <mbed.h>
#include <cmsis_os.h>
#include <USBHID.h>
#include <memory>

#include "SharedSPI.hpp"
#include "CC1201Radio.hpp"
#include "logger.hpp"
#include "pins.hpp"
#include "usb-interface.hpp"

using namespace std;

USBHID usbLink(64, 64, RJ_VENDOR_ID, RJ_PRODUCT_ID, RJ_RELEASE);

shared_ptr<RtosTimer> rx_led_ticker;
shared_ptr<RtosTimer> tx_led_ticker;

bool initRadio() {
    /// A shared spi bus used for the fpga and cc1201 radio
    shared_ptr<SharedSPI> sharedSPI =
        make_shared<SharedSPI>(RJ_SPI_MOSI, RJ_SPI_MISO, RJ_SPI_SCK);
    sharedSPI->format(8, 0);  // 8 bits per transfer

    // RX/TX leds
    auto rxTimeoutLED =
        make_shared<FlashingTimeoutLED>(DigitalOut(LED1, OpenDrain));
    auto txTimeoutLED =
        make_shared<FlashingTimeoutLED>(DigitalOut(LED2, OpenDrain));

    // Startup the CommModule interface
    CommModule::Instance = make_shared<CommModule>(rxTimeoutLED, txTimeoutLED);
    shared_ptr<CommModule> commModule = CommModule::Instance;

    // Create a new physical hardware communication link
    global_radio =
        new CC1201(sharedSPI, RJ_RADIO_nCS, RJ_RADIO_INT, preferredSettings,
                   sizeof(preferredSettings) / sizeof(registerSetting_t));

    return global_radio->isConnected();
}

void radioRxHandler(rtp::packet* pkt) {
    // TODO: copy data
    HID_REPORT data;
    bool success = usbLink.sendNB(&data);
    if (!success) {
        LOG(WARN, "Failed to transfer received packet over usb");
    }
}

int main() {
    if (initRadio()) {
        LOG(INIT, "Radio interface ready on %3.2fMHz!", global_radio->freq());

        CommModule::Instance->setRxHandler(&radioRxHandler, rtp::port::CONTROL);
        CommModule::Instance->setTxHandler(
            (CommLink*)global_radio, &CommLink::sendPacket, rtp::port::CONTROL);
    } else {
        LOG(FATAL, "No radio interface found!\r\n");
    }

    while (true) {
        HID_REPORT data;
        usbLink.readNB(&data);
        rtp::packet pkt;  // TODO: fill data
        CommModule::Instance->send(pkt);
    }
}
