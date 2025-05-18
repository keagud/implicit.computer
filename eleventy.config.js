import markdownIt from "markdown-it"
import markdownItFootnote from "markdown-it-footnote"
import slugify from '@sindresorhus/slugify';



export default async function(eleventyConfig) {

  eleventyConfig.setInputDirectory("src");
  eleventyConfig.setIncludesDirectory("_includes")
  eleventyConfig.setLayoutsDirectory("_layouts");

  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" })


  eleventyConfig.addCollection("posts", function(collectionApi) {
    // return collectionApi.getAll()
    const posts = collectionApi.getFilteredByGlob("src/blog/posts/*.md")

    return posts
  });

  eleventyConfig.addCollection("postTags", function(collectionApi) {
    const posts = collectionApi.getFilteredByGlob("src/blog/posts/*.md")

    const tagsSet = new Set(posts.map(p => p.data.tags).flat().map(t => t.toLowerCase()))
    console.log(tagsSet)
    return [...tagsSet]
  })



  eleventyConfig.addCollection("tagList", function(collection) {
    const tagSet = new Set();
    collection.getAll().forEach(item => {
      if ("tags" in item.data) {
        let tags = item.data.tags;
        if (typeof tags === "string") {
          tags = [tags];
        }
        tags.forEach(tag => tagSet.add(slugify(tag)));
      }
    });
    return [...tagSet].filter(tag => !["all", "nav", "post", "posts"].includes(tag));
  });


  eleventyConfig.addFilter("dateIso", date => {
    return date.toISOString();
  });

  eleventyConfig.addFilter("dateReadable", date => {
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  });


  let markdownOptions = {
    html: true, // Enable HTML tags in source
    breaks: true,  // Convert '\n' in paragraphs into <br>
    linkify: true // Autoconvert URL-like text to links
  };

  // configure the library with options
  let markdownLib = markdownIt(markdownOptions).use(markdownItFootnote);
  // set the library to process markdown files
  eleventyConfig.setLibrary("md", markdownLib);

};


