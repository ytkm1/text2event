chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "createEvent",
      title: "Create Event",
      contexts: ["selection"]
    });
  });

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "createEvent") {
    const selectedText = info.selectionText;
    processText(selectedText);
  }
});

function processText(text) {
  fetch('https://<server-url>/api/generate-url-YsQ8azA4', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-UUID': '<uuid>'
    },
    body: JSON.stringify({ text: text })
  })
  .then(response => response.json())
  .then(data => {
    openCalendarUrl(data.url);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function openCalendarUrl(url) {
  chrome.tabs.create({ url: url });
}
