// libs/posts.js
exports.getPosts = async (clientToken) => {
    // Dummy implementation
    console.log(`Getting posts with client token: ${clientToken}`);
    
    // Return dummy data
    return [
      {
        post_id: "post-123",
        title: "First Post",
        content: "This is post content",
        medias: [
          { media_id: "media-1", media_url: "https://example.com/image1.jpg" },
          { media_id: "media-2", media_url: "https://example.com/image2.jpg" }
        ]
      },
      {
        post_id: "post-456",
        title: "Second Post",
        content: "This is another post content",
        medias: [
          { media_id: "media-3", media_url: "https://example.com/image3.jpg" }
        ]
      }
    ];
  };
  
  exports.updatePosts = (postId, postData, callback) => {
    // Dummy implementation
    console.log(`Updating post with ID: ${postId}`);
    console.log('Post data:', JSON.stringify(postData));
    
    // Simulate a slight delay
    setTimeout(() => {
      if (Math.random() > 0.1) { // 90% success rate
        callback(null, { 
          success: true, 
          post_id: postId,
          updated_at: new Date().toISOString()
        });
      } else {
        // Simulate occasional errors
        callback(new Error(`Failed to update post ${postId}`), null);
      }
    }, 100);
  };
  
