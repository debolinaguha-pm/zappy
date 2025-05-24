# Zappy: A cool and simple project management tool!

---

## Step 1: Clone this repository

```bash
git clone <your-repo-url>
```

## Step 2: Create an environment

```bash
python -m venv venv
source venv/bin/activate
```

## Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the app

```bash
python app.py
```

## Step 5 (optional): Auto Start App

## ✅ Option 1: macOS — Automator App with Icon

### 🔧 Step-by-Step:

1. **Open Automator**
   - Launch Spotlight → search for “Automator”
   - Choose **New Document** → select **Application**

2. **Add "Run Shell Script"**
   - In the left panel, search for “Run Shell Script” and drag it to the right
   - Replace the default content with:

     ```bash
     cd /path/to/your/folder
     source venv/bin/activate
     python app.py &
     sleep 10
     open http://127.0.0.1:5000
     ```

3. **Save the App**
   - Save as: `Zappy.app`
   - Location: Desktop or Applications folder

4. **Set Custom Icon**
   - Right-click `.app` → **Get Info**
   - Open your logo image (`.png` or `.icns`) in Preview
   - Press `Cmd + C` to copy
   - In Get Info, click the small icon in the top-left and press `Cmd + V`

✅ Done! Double-click the app to launch Flask + browser. Shutdown is handled via your in-app button.

---

## 🐧 Option 2: Linux — .desktop Icon Launcher

### 🔧 Step-by-Step:

1. **Create a Shell Script**

   Save this as `start_app.sh` in your project folder:

   ```bash
   #!/bin/bash
   cd /home/youruser/path/to/your/folder
   source venv/bin/activate
   python app.py &
   sleep 10
   xdg-open http://127.0.0.1:5000
   ```

   Make it executable:

   ```bash
   chmod +x start_app.sh
   ```

2. **Create a `.desktop` File**

   Save this as `Zappy.desktop` in `~/.local/share/applications/` or on your Desktop:

   ```ini
   [Desktop Entry]
   Name=Zappy App
   Exec=/home/youruser/zappy-app/start_app.sh
   Icon=/home/youruser/zappy-app/static/img/logo.png
   Terminal=false
   Type=Application
   Categories=Utility;
   ```

   Make it executable:

   ```bash
   chmod +x Zappy.desktop
   ```

✅ Done! You now have a one-click app launcher with your logo as an icon.



