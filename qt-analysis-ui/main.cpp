#include "binarystreamer.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    BinaryStreamer w;
    w.show();

    return a.exec();
}
