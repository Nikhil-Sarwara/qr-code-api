using QRCoder.Core;

namespace QrCodeApi.Services;

public class QrCodeService
{
    public byte[] GenerateQrCode(string data, int pixelsPerModule = 20)
    {
        using QRCodeGenerator qrGenerator = new QRCodeGenerator();
        using QRCodeData qrCodeData = qrGenerator.CreateQrCode(data, QRCodeGenerator.ECCLevel.Q);
        using PngByteQRCode qrCode = new PngByteQRCode(qrCodeData);
        return qrCode.GetGraphic(pixelsPerModule);
    }
}