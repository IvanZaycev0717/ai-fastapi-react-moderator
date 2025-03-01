import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

const BASE_URL = "http://127.0.0.1:8000/comments/";

function App() {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    fetch(BASE_URL)
      .then((response) => response.json())
      .then((data) => setComments(data));
  }, []);

  return (
    <>
      {comments.map((comment) => (
        <div>
          <p>
            Пользователь {comment.username} оставил комментарий в {comment.date}
            :
          </p>
          <p>{comment.censored_text}</p>
        </div>
      ))}
    </>
  );
}

export default App;
