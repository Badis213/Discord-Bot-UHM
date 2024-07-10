# Error Log for Discord Bot UHM

## July 9, 2024

### Issue: Unable add the unverified member role
- **Description**: The bot can't add a role to a member (unverified member role) when someone joins.
- **Solution**: Checked the permissions. Setted the BOT role over the MEMBER role. Bot successfully added role.

### Issue: Welcome Message Not Sending
- **Description**: The welcome message did not send when a new member joined the server.
- **Error Message**: No specific error message; message simply didn't appear.
- **Solution**: Debugged code and found incorrect channel ID in `on_member_join` event handler. Updated channel ID and tested successfully.

## July 10, 2024

### Issue: Welcome Message Not Sending
- **Desription**: The welcome message did not send when a new user joined the server.
- **Error Message**:
    ""
  File "\OneDrive\Bureau\Utahime Project\src\main.py", line 55, in on_member_join
    background = Editor("Assets\\welcome-back.jpg")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'Assets\\welcome-back.jpg'""
- **Solution**: using os path function to add 'src' folder to the path.