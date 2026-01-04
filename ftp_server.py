# ===================== YOUR ORIGINAL FTP CODE (UNCHANGED) =====================
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import socket

FTP_ROOT = "ftp_root"
os.makedirs(FTP_ROOT, exist_ok=True)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "123", FTP_ROOT, perm="elradfmwMT")
    authorizer.add_anonymous(FTP_ROOT, perm="elradfmwMT")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."

    address = ('0.0.0.0', 2121)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    ip = get_ip_address()
    print(f"\n{'='*40}")
    print(f"FTP Server Running on {ip}:2121")
    print(f"Username: user")
    print(f"Password: 123")
    print(f"Or use Anonymous login")
    print(f"Target Directory: {os.path.abspath(FTP_ROOT)}")
    print(f"{'='*40}\n")

    server.serve_forever()

# ===================== STREAMLIT PART (ADDED ONLY) =====================
import streamlit as st
import threading
import qrcode
import io

def run_streamlit():
    st.set_page_config(page_title="FTP File Manager")
    st.title("📂 FTP + Browser File Transfer")

    ip = get_ip_address()
    ftp_url = f"ftp://user:123@{ip}:2121"

    # Start FTP server ONCE
    if "ftp_started" not in st.session_state:
        threading.Thread(target=start_ftp_server, daemon=True).start()
        st.session_state.ftp_started = True

    st.success("FTP Server is running")
    st.code(ftp_url)

    # ---- QR CODE ----
        # ---- QR CODE (FAST & COMPATIBLE) ----
    ftp_qr_text = f"ftp://{ip}:2121"

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(ftp_qr_text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")

    st.image(
        buf.getvalue(),
        caption="Scan QR → enter username: user | password: 123",
        width=300
    )

    st.code(ftp_qr_text)

    # ---- FILE MANAGER ----
    st.subheader("📁 Files on PC")

    uploaded = st.file_uploader("Upload files", accept_multiple_files=True)
    if uploaded:
        for f in uploaded:
            with open(os.path.join(FTP_ROOT, f.name), "wb") as out:
                out.write(f.getbuffer())
        st.success("Upload complete")

    for name in os.listdir(FTP_ROOT):
        path = os.path.join(FTP_ROOT, name)
        col1, col2, col3 = st.columns([4, 1, 1])

        col1.write(name)

        if os.path.isfile(path):
            with open(path, "rb") as f:
                col2.download_button("⬇️", f, file_name=name)

        if col3.button("🗑️", key=name):
            os.remove(path)
            st.experimental_rerun()

# ===================== ENTRY POINT =====================
if __name__ == "__main__":
    run_streamlit()
