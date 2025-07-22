import React, { useEffect, useState } from "react";
import httpClient from "../httpClient";
import { useAuth } from "../contexts/authContext";
import StreamerCard from "../components/StreamerCard.jsx";

const Favorites = () => {
    const [favStreamers, setFav] = useState([]);
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getStreamers = async () => {
            try {
                const res = await httpClient.get("http://localhost:5000/favorites");
                setFav(res.data.favorites);
            } catch (err) {
                console.error("Failed to load favorites:", err);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            getStreamers();
        } else {
            setLoading(false);
        }
    }, [user]);

    if (loading) return <p>Loading...</p>;
    if (!user) return <p>Please log in to see your favorite streamers.</p>;

    const unfav = async (streamer) => {
        try {
            await httpClient.post("http://localhost:5000/unfollow", { streamer: streamer });
            setFav((prev) => prev.filter((s) => s.id !== streamer.id));
        } catch (err) {
            console.error("Failed to unfollow", err);
        }
    };

    return (
  <div>
    <a href="/dashboard">
      <button>Dashboard</button>
    </a>
    <div className="grid-container">
      {favStreamers.map((streamer) => (
          <div className="grid-item" key={streamer.id}>
              <StreamerCard streamer={streamer}/>
              <button onClick={() => unfav(streamer)}>Unfollow</button>
          </div>
      ))}
    </div>
  </div>
    );

};

export default Favorites;
