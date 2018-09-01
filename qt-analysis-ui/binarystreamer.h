#ifndef BINARYSTREAMER_H
#define BINARYSTREAMER_H

#include <QWidget>
#include <QFileDialog>
#include <QDebug>
#include <QProcess>
#include <QDateTime>

namespace Ui {
class BinaryStreamer;
}

class BinaryStreamer : public QWidget
{
    Q_OBJECT

public:
    explicit BinaryStreamer(QWidget *parent = 0);
    ~BinaryStreamer();

private slots:
    void on_TypeBox_currentTextChanged(const QString &arg1);

    void on_ScanStartBox_valueChanged(int arg1);

    void on_ScanEndBox_valueChanged(int arg1);

    void on_NumCyclesBox_valueChanged(int arg1);

    void on_GasStepsBox_valueChanged(int arg1);

    void on_FrameBox_valueChanged(int arg1);

    void on_DarkBox_valueChanged(int arg1);

    void on_PumpOnBox_valueChanged(int arg1);

    void on_InputButton_clicked();

    void on_OutputButton_clicked();

    void on_RawTextCheckBox_clicked(bool checked);

    void on_dODBox_clicked(bool checked);

    void on_ClearButton_clicked();

    void on_SaveButton_clicked();

    void on_PrefixBox_textEdited(const QString &arg1);

    void on_RunButton_clicked();

    void on_AttoCubeCheck_clicked(bool checked);

    void on_OffsetBox_valueChanged(double arg1);

    void on_InputField_textEdited(const QString &arg1);

    void on_OutputField_textEdited(const QString &arg1);

    void on_LogButton_clicked();

    void on_LogField_textEdited(const QString &arg1);

private:
    void calcStatic(void);
    void printText(void);
    void loadlog(void);
    void streamBinary(void);
    void textToBinary(void);
    void dODCalc(void);
    Ui::BinaryStreamer *ui;
    short CalcType;
    bool InputType; // 0: binary; 1: text
    bool CalcdODBool; // 0: no; 1: yes
    bool ACUse;
    enum{
        STATIC,
        DYNAMIC
    };
    QString ScriptPath;
    QString GasPath;
    QString PumpOnPath;
    QString PumpOffPath;
    QString PythonPath;
    QString BinDir;
    QString SourceDir;
    QString LogDir;
    QString directory;
    QString outdir;
    QString Prefix;
    QString logpath;

    int StartScan;
    int EndScan;
    int NumCycles;
    int NumDark;
    int NumBG;
    int NumScan;
    int NumGas;
    int NumFrames;
    int NumSteps;
    double TimeOffset;
};

#endif // BINARYSTREAMER_H
