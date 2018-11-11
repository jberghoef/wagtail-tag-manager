import TagManager from "./components/tag_manager";

document.onreadystatechange = () => {
  if (document.readyState === "complete") {
    new TagManager();
  }
};
