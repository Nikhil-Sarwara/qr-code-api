using Microsoft.AspNetCore.Mvc;
using QrCodeApi.Services;

namespace QrCodeApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class QrCodeController(QrCodeService qrCodeService) : ControllerBase
{
    [HttpGet]
    public IActionResult GenerateQrCode([FromQuery] string data, [FromQuery] int size = 20)
    {
        if (string.IsNullOrEmpty(data)) return BadRequest("Data parameter is required");

        var qrCodeBytes = qrCodeService.GenerateQrCode(data, size);
        return File(qrCodeBytes, "image/png");
    }
}