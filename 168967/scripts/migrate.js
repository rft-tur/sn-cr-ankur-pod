const getPosts = require('../libs/posts.js').getPosts;  
const r2 = require('../libs/r2.js');  
const updatePost = require('../libs/posts.js').updatePosts;  
const dotenv = require('dotenv');  
dotenv.config();  

// Promisified R2 upload wrapper  
const uploadR2Promise = (url) => {  
  return new Promise((resolve, reject) => {  
    r2.uploadR2(url, (err, newUrl) => {  
      if (err) reject(err);  
      else resolve(newUrl);  
    });  
  });  
};  
  
// Promisified post update wrapper  
const updatePostPromise = (postId, postData) => {  
  return new Promise((resolve, reject) => {  
    updatePost(postId, postData, (err, data) => {  
      if (err) reject(err);  
      else resolve(data);  
    });  
  });  
};  
  
async function ProcessUpload(post) {  
  try {  
    // Upload all images in parallel  
    const uploadPromises = post.medias.map(media =>  
      uploadR2Promise(media.media_url)  
    );  
    const newUrls = await Promise.all(uploadPromises);  
  
    // Update media URLs  
    post.medias.forEach((media, index) => {  
      media.media_url = newUrls[index];  
    });  
  
    // Save updated post  
    await updatePostPromise(post.post_id, post);  
    console.log(`Updated post: ${post.post_id}`);  
  } catch (error) {  
    console.error(`Failed processing post ${post.post_id}:`, error);  
  }  
}  
  
async function Main() {  
  let clientToken = process.env.CLIENT_TOKEN;  
  
  try {  
    let posts = await getPosts(clientToken);  
  
    // Process posts sequentially  
    for (let post of posts) {  
      await ProcessUpload(post);  
    }  
  } catch (error) {  
    console.error('Main execution failed:', error);  
  }  
}  
  
Main();  