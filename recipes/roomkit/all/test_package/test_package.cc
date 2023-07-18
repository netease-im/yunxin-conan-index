#include <iostream>
#include "room_kit_interface.h"

int main(int argc, char* argv[]) {
    auto* roomkit = neroom::createNERoomKit();
    auto version = roomkit->getSdkVersions();
    std::cout << "roomkit version: " << version.roomKitVersion << std::endl;
    neroom::destroyNERoomKit();
    return 0;
}
