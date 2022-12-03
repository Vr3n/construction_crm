let defaultTransitionDuration = 500;
let defaultMessageTimeout = 4000;

const hDispatch = (eventName, params = {}) =>
  window.dispatchEvent(new CustomEvent(eventName, { detail: params }));

const hStatusMessageDisplay = (
  message,
  messageType = "info",
  timeout = undefined,
  eventName = undefined
) =>
  window.dispatchEvent(
    new CustomEvent("status-message-display", {
      detail: {
        message,
        messageType,
        timeout,
        eventName,
      },
    })
  );