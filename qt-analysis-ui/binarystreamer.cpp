#include "binarystreamer.h"
#include "ui_binarystreamer.h"

BinaryStreamer::BinaryStreamer(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::BinaryStreamer)
{
    CalcType=DYNAMIC;
    InputType=0;
    NumCycles=1;
    NumFrames=1;
    NumGas=0;
    ACUse=0;
    TimeOffset=10;

    ScriptPath="C:/Users/D60 South/Desktop/HungTzuScripts/";
    BinDir="C:/Users/D60 South/Desktop/binary-data/";
    SourceDir="C:/Users/D60 South/Desktop/1093DATA/";
    LogDir="C:/Users/D60 South/Desktop/MeasurementLog/";
    PythonPath="python";

    ui->setupUi(this);
    ui->NumStepsBox->setReadOnly(true);
    ui->ProgramOutputBox->setReadOnly(true);
    //ui->ProgramOutputBox->appendPlainText("strand\nstrand");
}

BinaryStreamer::~BinaryStreamer()
{
    delete ui;
}

void BinaryStreamer::on_TypeBox_currentTextChanged(const QString &arg1)
{
    //ui->ProgramOutputBox->appendPlainText(arg1);
    if(arg1=="Static")
        CalcType=STATIC;
    if(arg1=="Dynamic")
        CalcType=DYNAMIC;
    ui->ProgramOutputBox->appendPlainText(QString::number(CalcType));
}

void BinaryStreamer::on_ScanStartBox_valueChanged(int arg1)
{
    StartScan=arg1;
}

void BinaryStreamer::on_ScanEndBox_valueChanged(int arg1)
{
    EndScan=arg1;
}

void BinaryStreamer::on_NumCyclesBox_valueChanged(int arg1)
{
    NumCycles=arg1;
}

void BinaryStreamer::on_GasStepsBox_valueChanged(int arg1)
{
    NumGas=arg1;
}

void BinaryStreamer::on_FrameBox_valueChanged(int arg1)
{
    NumFrames=arg1;
}

void BinaryStreamer::on_DarkBox_valueChanged(int arg1)
{
    NumDark=arg1;
}

void BinaryStreamer::on_PumpOnBox_valueChanged(int arg1)
{
    NumBG=arg1;
}

void BinaryStreamer::on_InputButton_clicked()
{
    directory = QFileDialog::getExistingDirectory(this,
                            tr("Find Files"), SourceDir);
    ui->InputField->setText(directory);
}

void BinaryStreamer::on_OutputButton_clicked()
{
    outdir = QFileDialog::getExistingDirectory(this,
                            tr("Find Files"), BinDir);
    ui->OutputField->setText(outdir);
}

void BinaryStreamer::on_RawTextCheckBox_clicked(bool checked)
{
    InputType=checked;
}

void BinaryStreamer::on_dODBox_clicked(bool checked)
{
    CalcdODBool=checked;
}

void BinaryStreamer::on_ClearButton_clicked()
{
    ui->ProgramOutputBox->clear();
    ui->NumStepsBox->clear();
}

void BinaryStreamer::on_SaveButton_clicked()
{
    QString fname=QFileDialog::getSaveFileName(this,tr("Save File"),BinDir,tr("Text files (*.txt)"));
    QFile filesave(fname);
    if (!filesave.open(QIODevice::WriteOnly | QIODevice::Text))
        return;

    QTextStream out(&filesave);
    out << ui->ProgramOutputBox->toPlainText() << "\n";
    //qDebug()<<fname;//ui->ProgramOutputBox->toPlainText();
    filesave.close();
}


void BinaryStreamer::on_PrefixBox_textEdited(const QString &arg1)
{
    Prefix=arg1;
}

void BinaryStreamer::calcStatic(void)
{
    QProcess callpy;
    QStringList params;
    QString CalcPath=ScriptPath+QString("/calcStatic.py");
    QDir::setCurrent(directory);
    params<<CalcPath<<Prefix<<QString::number(StartScan)<<QString::number(EndScan)<<QString::number(NumDark)<<QString::number(NumBG);
    callpy.start(PythonPath,params);
    callpy.waitForFinished(-1);
    ui->ProgramOutputBox->appendPlainText("#Calc Static Output:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardOutput());
    ui->ProgramOutputBox->appendPlainText("#Calc Static Error:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardError());
    callpy.close();
    QString onname=Prefix+tr("_pumpon.npy");
    QString offname=Prefix+tr("_pumpoff.npy");

    QString darkname=Prefix+tr("_dark.npy");
    QString staticname=Prefix+tr("-static.npy");
    QString dODname=Prefix+tr("-dOD.npy");
    QFile::copy(QString(onname),outdir+QString("/")+QString(onname));
    QFile::copy(QString(offname),outdir+QString("/")+QString(offname));
    //QFile::copy(QString(gasname),outdir+QString("/")+QString(gasname));
    QFile::copy(QString(darkname),outdir+QString("/")+QString(darkname));
    //QFile::copy(QString(bgname),outdir+QString("/")+QString(bgname));
    QFile::copy(QString(staticname),outdir+QString("/")+QString(staticname));
    QFile::copy(QString(dODname),outdir+QString("/")+QString(dODname));
}

void BinaryStreamer::printText(void)
{
    ui->ProgramOutputBox->appendPlainText("####################################");
    ui->ProgramOutputBox->appendPlainText("########## New Output File #########");
    ui->ProgramOutputBox->appendPlainText("####################################");
    ui->ProgramOutputBox->appendPlainText(QString("Prefix = ")+Prefix);
    ui->ProgramOutputBox->appendPlainText(QString("Start = ")+QString::number(StartScan));
    ui->ProgramOutputBox->appendPlainText(QString("End = ")+QString::number(EndScan));
    ui->ProgramOutputBox->appendPlainText(QString("NumCycles = ")+QString::number(NumCycles));
    ui->ProgramOutputBox->appendPlainText(QString("NumSteps = ")+QString::number(NumSteps));
    ui->ProgramOutputBox->appendPlainText(QString("NumGas = ")+QString::number(NumGas));
    ui->ProgramOutputBox->appendPlainText(QString("Dark = ")+QString::number(NumDark));
    ui->ProgramOutputBox->appendPlainText(QString("PumpOn = ")+QString::number(NumBG));
    ui->ProgramOutputBox->appendPlainText(QString("Input = ")+directory);
    ui->ProgramOutputBox->appendPlainText(QString("Output = ")+outdir);
    QDateTime UTC(QDateTime::currentDateTimeUtc());
    ui->ProgramOutputBox->appendPlainText(QString("# ")+UTC.toString());
    ui->ProgramOutputBox->appendPlainText("############# Start Logging ###########\n");
}

void BinaryStreamer::loadlog(void)
{
    QProcess callpy;
    QStringList params;
    QString CalcPath;
    QDir::setCurrent(outdir);
    if(!ACUse)
        CalcPath=ScriptPath+QString("/loadlog.py");
    else
        CalcPath=ScriptPath+QString("/loadlogAC.py");

//QString logpath=directory+QString("/Log.dat");
    params<<CalcPath<<logpath<<Prefix<<QString::number(StartScan)<<QString::number(EndScan)<<QString::number(NumCycles)<<QString::number(TimeOffset);
    callpy.start(PythonPath,params);
    callpy.waitForFinished(-1);
    //qDebug()<<params;
    //QString p_stdout(callpy.readAllStandardOutput());
    //QString p_stderr(callpy.readAllStandardError());
    //qDebug()<<p_stdout;
    ui->ProgramOutputBox->appendPlainText("#Load Log Output:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardOutput());
    ui->ProgramOutputBox->appendPlainText("#Load Log Error:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardError());
    callpy.close();
}

void BinaryStreamer::streamBinary(void)
{
    QProcess callpy;
    QStringList params;
    QString CalcPath=ScriptPath+QString("/calcBinary.py");
    QDir::setCurrent(directory);
    params<<CalcPath<<outdir<<Prefix<<QString::number(NumCycles)<<QString::number(NumSteps)<<QString::number(NumGas)<<QString::number(NumDark)<<QString::number(NumBG);
    callpy.start(PythonPath,params);
    callpy.waitForFinished(-1);
    ui->ProgramOutputBox->appendPlainText("#Load Log Output:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardOutput());
    ui->ProgramOutputBox->appendPlainText("#Load Log Error:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardError());
    callpy.close();
    QString onname=Prefix+tr("_pumpon.npy");
    QString offname=Prefix+tr("_pumpoff.npy");
    QString gasname=Prefix+tr("_gas_raw.npy");
    QString darkname=Prefix+tr("_dark.npy");
    QString bgname=Prefix+tr("_bg.npy");
    QString gas_ODname=Prefix+tr("-gas_dOD.npy");
    QString dODname=Prefix+tr("-dOD.npy");
    QFile::copy(QString(onname),outdir+QString("/")+QString(onname));
    QFile::copy(QString(offname),outdir+QString("/")+QString(offname));
    QFile::copy(QString(gasname),outdir+QString("/")+QString(gasname));
    QFile::copy(QString(darkname),outdir+QString("/")+QString(darkname));
    QFile::copy(QString(bgname),outdir+QString("/")+QString(bgname));
    QFile::copy(QString(gas_ODname),outdir+QString("/")+QString(gas_ODname));
    QFile::copy(QString(dODname),outdir+QString("/")+QString(dODname));
}

void BinaryStreamer::textToBinary(void)
{
    QProcess callpy;
    QStringList params;
    QString EXEPath=ScriptPath+QString("/TextStreamerConsole/TextStreamerConsole.exe");
    PumpOnPath=outdir+QString("/")+Prefix+QString("_pumpon.txt");
    PumpOffPath=outdir+QString("/")+Prefix+QString("_pumpoff.txt");
    GasPath=outdir+QString("/")+Prefix+QString("_gas.txt");
    QDir::setCurrent(directory);
    params<<Prefix<<PumpOffPath<<PumpOnPath<<GasPath<<QString::number(NumGas*NumCycles)<<QString::number(NumSteps*NumCycles);
    callpy.start(EXEPath,params);
    callpy.waitForFinished(-1);
    ui->ProgramOutputBox->appendPlainText("#Text2Binary Log Output:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardOutput());
    ui->ProgramOutputBox->appendPlainText("#Text2Binary Log Error:\n");
    ui->ProgramOutputBox->appendPlainText(callpy.readAllStandardError());
    callpy.close();

    QString onname=Prefix+tr("_pumpon_raw.bin");
    QString offname=Prefix+tr("_pumpoff_raw.bin");
    QString gasname=Prefix+tr("_gas_raw.bin");
    QFile::copy(QString(onname),outdir+QString("/")+QString(onname));
    QFile::copy(QString(offname),outdir+QString("/")+QString(offname));
    QFile::copy(QString(gasname),outdir+QString("/")+QString(gasname));
    QFile::copy(QString("Scan")+QString::number(NumDark)+QString(".dat"),outdir+QString("/")+Prefix+QString(".dark"));
    QFile::copy(QString("Scan")+QString::number(NumBG)+QString(".dat"),outdir+QString("/")+Prefix+QString(".bg"));
}

void BinaryStreamer::on_RunButton_clicked()
{
    NumSteps=((EndScan-StartScan+1)/NumCycles - NumGas)/2;
    if(((EndScan-StartScan+1)/NumCycles - NumGas)%2){
        ui->ProgramOutputBox->appendPlainText(QString::number(((EndScan-StartScan+1)/NumCycles - NumGas)%2));
        ui->ProgramOutputBox->appendPlainText(QString("Start = ")+QString::number(StartScan));
        ui->ProgramOutputBox->appendPlainText(QString("End = ")+QString::number(EndScan));
        ui->ProgramOutputBox->appendPlainText(QString("NumCycles = ")+QString::number(NumCycles));
        ui->ProgramOutputBox->appendPlainText(QString("NumSteps = ")+QString::number(NumSteps));
        ui->ProgramOutputBox->appendPlainText(QString("NumGas = ")+QString::number(NumGas));
        ui->ProgramOutputBox->appendPlainText(QString("Dark = ")+QString::number(NumDark));
        ui->ProgramOutputBox->appendPlainText("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        ui->ProgramOutputBox->appendPlainText("!!!!!!!!!!! Wrong Numbers !!!!!!!!!!");
        ui->ProgramOutputBox->appendPlainText("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        return;
    }
    ui->NumStepsBox->setText(QString::number(NumSteps));

    if(CalcType==STATIC){
        if(InputType){
            ui->ProgramOutputBox->appendPlainText("!!! Text iutput for static not supported yet !!!\n");
            return;
        }
        printText();
        ui->ProgramOutputBox->appendPlainText("############# Start Static ###########\n");
        calcStatic();
        return;
    }
    printText();
    loadlog();
    if(!InputType)
        streamBinary();
    else
        textToBinary();

}

void BinaryStreamer::on_AttoCubeCheck_clicked(bool checked)
{
    ACUse=checked;
}

void BinaryStreamer::on_OffsetBox_valueChanged(double arg1)
{
    TimeOffset=arg1;
}

void BinaryStreamer::on_InputField_textEdited(const QString &arg1)
{
    directory=arg1;
}

void BinaryStreamer::on_OutputField_textEdited(const QString &arg1)
{
    outdir=arg1;
}

void BinaryStreamer::on_LogButton_clicked()
{
    logpath = QFileDialog::getOpenFileName(this,
                            tr("Find Files"), LogDir);
    ui->LogField->setText(logpath);
}

void BinaryStreamer::on_LogField_textEdited(const QString &arg1)
{
    logpath=arg1;
}
