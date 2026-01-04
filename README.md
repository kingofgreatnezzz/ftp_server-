# Local FTP Server

This purely uses the FTP protocol to transfer files from your phone to PC without internet.

## Setup

1.  **Install Dependency**:
    ```bash
    pip install pyftpdlib
    ```

2.  **Run Server**:
    ```bash
    python ftp_server.py
    ```

3.  **Connect from Phone**:
    You can use a dedicated app like **Owlfiles** OR try your phone's built-in File Manager (Files app on iOS, My Files on Android).

    *   **Host**: (The IP printed on your screen)
    *   **Port**: `2121`
    *   **User**: `user`
    *   **Pass**: `123`
    *   **Directory**: Files will be saved in the `ftp_root` folder on your PC.
