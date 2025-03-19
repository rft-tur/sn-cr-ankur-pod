// libs/r2.js
exports.uploadR2 = (url, callback) => {
  // Dummy implementation
  console.log(`Uploading file from URL: ${url}`);

  // Simulate a slight delay
  setTimeout(() => {
    if (Math.random() > 0.05) { // 95% success rate
      // Generate a dummy R2 URL
      const r2Url = `https://r2-storage.example.com/${Date.now()}-${url.split('/').pop()}`;
      callback(null, r2Url);
    } else {
      // Simulate occasional errors
      callback(new Error(`Failed to upload file from ${url}`), null);
    }
  }, 200);
};