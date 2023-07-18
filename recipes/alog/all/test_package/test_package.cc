#include <iostream>
#include "alog.h"

#define YXLOGEnd ALOGEnd
#define YXLOG(level) ALOG_DIY("app", LogNormal, level)

int main(int argc, char* argv[]) {
    YXLOG(Info) << "Hello, Alog!" << YXLOGEnd;
    return 0;
}
