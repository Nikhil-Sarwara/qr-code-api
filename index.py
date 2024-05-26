from flask import Flask, request, jsonify, send_file
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
# Default Color Blue
@app.route('/api/color-customized/qr', methods=['POST'])
def generate_color_customized_qr_code():
    try:
        data = request.json.get('text', '')
        fill_color = request.json.get('fill_color', 'blue')
        back_color = request.json.get('back_color', 'white')

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

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# Styled QR Code
@app.route('/api/styled/qr', methods=['POST'])
def generate_styled_qr_code():
    try:
        data = request.json.get('text', '')
        fill_color = request.json.get('fill_color', 'blue')
        back_color = request.json.get('back_color', 'white')
        module_shape = request.json.get('module_shape', 'default')

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

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        if module_shape == 'rounded':
            img = StyledPilImage(img, md.RoundedModuleDrawer())
        elif module_shape == 'circle':
            img = StyledPilImage(img, md.CircleModuleDrawer())
        elif module_shape == 'square':
            img = StyledPilImage(img, md.SquareModuleDrawer())
        elif module_shape == 'gapped-square':
            img = StyledPilImage(img, md.GappedSquareModuleDrawer())
        elif module_shape == 'vertical-bars':
            img = StyledPilImage(img, md.VerticalBarsDrawer())
        elif module_shape == 'horizontal-bars':
                img = StyledPilImage(img, md.HorizontalBarsDrawer())
        else:
            img = StyledPilImage(img, md.SquareModuleDrawer())

        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
