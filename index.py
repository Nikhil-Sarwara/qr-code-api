from flask import Flask, request, send_file, jsonify
import qrcode
from qrcode.image.styledpil import StyledPilImage
import qrcode.image.styles.moduledrawers as md
import qrcode.image.styles.colormasks as cm
from io import BytesIO
from PIL import Image
import requests

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
        gradient_type = request.json.get('gradient_type', 'none')
        module_shape = request.json.get('module_shape', 'default')
        eye_shape = request.json.get('eye_shape', 'default')
        logo_url = request.json.get('logo_url', None)

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

        # Set color mask based on gradient type
        color_mask = None
        if gradient_type == 'radial':
            color_mask = cm.RadialGradiantColorMask(
                back_color=back_color,
                center_color=fill_color,
                edge_color=(255, 255, 255)
            )
        elif gradient_type == 'horizontal':
            color_mask = cm.HorizontalGradiantColorMask(
                back_color=back_color,
                left_color=fill_color,
                right_color=(255, 255, 255)
            )
        elif gradient_type == 'vertical':
            color_mask = cm.VerticalGradiantColorMask(
                back_color=back_color,
                top_color=fill_color,
                bottom_color=(255, 255, 255)
            )
        else:
            color_mask = cm.SolidFillColorMask(
                front_color=fill_color,
                back_color=back_color
            )

        # Generate the QR code image with the specified drawers and colors
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            eye_drawer=eye_drawer,
            color_mask=color_mask
        )

        # Add logo if provided
        if logo_url:
            response = requests.get(logo_url)
            logo = Image.open(BytesIO(response.content))
            img = add_logo(img, logo)

        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

# Add logo to QR code
def add_logo(qr_img, logo):
    # Ensure logo has an alpha layer
    if logo.mode in ('RGBA', 'LA') or (logo.mode == 'P' and 'transparency' in logo.info):
        alpha = logo.convert('RGBA').split()[3]
        logo = logo.convert('RGB').convert('RGBA')
        logo.putalpha(alpha)
    else:
        logo = logo.convert('RGBA')

    # Calculate the size of the logo
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width / 4)
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Position the logo in the center of the QR code
    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    qr_img.paste(logo, pos, logo)

    return qr_img