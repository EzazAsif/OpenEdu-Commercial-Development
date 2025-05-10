window.onload = function () {
  // Generate a Token by calling a method.
  // @param 1: appID
  // @param 2: serverSecret
  // @param 3: Room ID
  // @param 4: User ID
  // @param 5: Username

  const appID = 1297075164;
  const serverSecret = "643355924e77f8301a5d74ad6be1e81d";
  const kitToken = ZegoUIKitPrebuilt.generateKitTokenForTest(
    appID,
    serverSecret,
    roomID,
    userID,
    userName
  );

  const zp = ZegoUIKitPrebuilt.create(kitToken);
  zp.joinRoom({
    container: document.querySelector("#root"),
    sharedLinks: [
      {
        name: "Personal link",
        url:
          window.location.protocol +
          "//" +
          window.location.host +
          window.location.pathname +
          "?roomID=" +
          roomID,
      },
    ],
    scenario: {
      mode: ZegoUIKitPrebuilt.VideoConference,
    },

    turnOnMicrophoneWhenJoining: false,
    turnOnCameraWhenJoining: false,
    showMyCameraToggleButton: true,
    showMyMicrophoneToggleButton: true,
    showAudioVideoSettingsButton: true,
    showScreenSharingButton: true,
    showTextChat: true,
    showUserList: true,
    maxUsers: 50,
    layout: "Sidebar",
    showLayoutButton: true,
  });
};
