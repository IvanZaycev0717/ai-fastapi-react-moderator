import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

const BASE_URL = "http://127.0.0.1:8000/comments/";

function App() {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [username, setUsername] = useState("");
  const [commentId, setCommentId] = useState(0);

  useEffect(() => {
    fetch(BASE_URL)
      .then((response) => response.json())
      .then((data) => setComments(data));
  }, []);

  const publishComment = (event) => {
    event?.preventDefault();
    const json_string = JSON.stringify({
      username,
      original_text: newComment,
    });

    if (commentId === 0) {
      const requestOptions = {
        method: "POST",
        headers: new Headers({ "Content-Type": "application/json" }),
        body: json_string,
      };
      fetch(BASE_URL, requestOptions)
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => fetchComments())
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          setNewComment("");
          setUsername("");
        });
    } else {
      fetch(BASE_URL + `${commentId}/edit/${newComment}`, { method: "PUT" })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => fetchComments())
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          setNewComment("");
          setUsername("");
          setCommentId(0);
        });
    }
  };

  const handleDeleteComment = (comment_id) => {
    fetch(BASE_URL + comment_id, { method: "DELETE" })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => fetchComments())
      .catch((error) => {
        alert(error);
      });
  };

  const handleEditComment = (comment_id) => {
    fetch(BASE_URL + comment_id)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => {
        setUsername(data.username);
        setNewComment(data.censored_text);
        setCommentId(data.id);
      })
      .catch((error) => {
        alert(error);
      });
  };

  const fetchComments = () => {
    fetch(BASE_URL)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => setComments(data))
      .catch((error) => console.log(error));
  };

  return (
    <>
      {comments.map((comment) => (
        <div key={comment.id}>
          <p>
            Пользователь {comment.username} оставил комментарий в {comment.date}
            :
          </p>
          <p>{comment.censored_text}</p>
          <button onClick={() => handleEditComment(comment.id)}>
            Редактировать
          </button>
          <button onClick={() => handleDeleteComment(comment.id)}>
            Удалить
          </button>
        </div>
      ))}
      <div>
        <form className="comment-form">
          <input
            className="comment-form__input"
            type="text"
            placeholder="Напишите ваше имя"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            className="comment-form__input"
            type="text"
            placeholder="Напишите комментарий"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
          />
          <button
            className="comment-form__button"
            type="submit"
            disabled={!newComment || !username}
            onClick={publishComment}
          >
            Опубликовать
          </button>
        </form>
      </div>
    </>
  );
}

export default App;
