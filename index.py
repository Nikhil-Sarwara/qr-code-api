from flask import Flask, request, send_file, jsonify
import qrcode
from qrcode.image.styledpil import StyledPilImage
import qrcode.image.styles.moduledrawers as md
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Basic QR Code
@app.route('/api/basic/qr', methods=['POST'])
def generate_qr_code():
    try:
        data = request.json.get('text', '')
        if not data:
            return jsonify({'error': 'No text provided'}), 400

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Color Customized QR Code
@app.route('/api/advanced/qr', methods=['POST'])
def generate_advanced_qr_code():
    try:
        data = request.json.get('text', '')
        fill_color = tuple(request.json.get('fill_color', [0, 0, 0]))
        back_color = tuple(request.json.get('back_color', [255, 255, 255]))
        module_shape = request.json.get('module_shape', 'default')
        eye_shape = request.json.get('eye_shape', 'default')

        if not data:
            return jsonify({'error': 'No text provided'}), 400

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        # Set module drawer
        module_drawer = None
        if module_shape == 'rounded':
            module_drawer = md.RoundedModuleDrawer()
        elif module_shape == 'circle':
            module_drawer = md.CircleModuleDrawer()
        elif module_shape == 'square':
            module_drawer = md.SquareModuleDrawer()
        elif module_shape == 'gapped-square':
            module_drawer = md.GappedSquareModuleDrawer()
        elif module_shape == 'vertical-bars':
            module_drawer = md.VerticalBarsDrawer()
        elif module_shape == 'horizontal-bars':
            module_drawer = md.HorizontalBarsDrawer()

        # Set eye drawer
        eye_drawer = None
        if eye_shape == 'rounded':
            eye_drawer = md.RoundedModuleDrawer()
        elif eye_shape == 'dots':
            eye_drawer = md.CircleModuleDrawer()

        # Generate the QR code image with the specified drawers and colors
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            eye_drawer=eye_drawer,
            color_mask=qrcode.image.styles.colormasks.SolidFillColorMask(
                front_color=fill_color,
                back_color=back_color
            )
        )

        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
