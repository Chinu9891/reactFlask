import httpClient from "../httpClient";
import React, {useEffect, useState} from "react";
import StreamerCard from "../components/StreamerCard.jsx";
import NavBar from "../components/NavBar.jsx";
import "./dashboard.css"

const Dashboard = () => {
    const [streamers, setStreamers] = useState([]);
    const [followedID, setFollowedID] = useState([]);
    const [searchFav, setSearchFav] = useState("");
    const [search, setSearch] = useState(null);
    const [searchInput, setSearchInput] = useState("");


    useEffect(() => {
        const loadFollowed = async () => {
            try {
                const res = await httpClient.get("http://localhost:5000/favorites");
                const data = res.data.favorites;
                setFollowedID(data.map(streamer => streamer.id));
            } catch (err) {
                console.log("Error loading favorites", err);
            }
        };

        loadFollowed();
    }, []);

    useEffect(() => {
        const loadFeatured = async () => {
            try {
                const res = await httpClient.get("http://localhost:5000/featured");
                setStreamers(res.data);
            } catch (err) {
                console.error("Error fetching featured streamers:", err);
            }
        };

        loadFeatured();
    }, []);

    const fav = async (streamer) => {
        try {
            await httpClient.post("http://localhost:5000/follow", { streamer: streamer });
            setFollowedID((prev) => [...prev, streamer.id]);
        } catch (err) {
            console.error("Failed to follow", err);
        }
    };

    const unfav = async (streamer) => {
        try {
            await httpClient.post("http://localhost:5000/unfollow", { streamer: streamer });
            setFollowedID((prev) => prev.filter((sid) => sid !== streamer.id));
        } catch (err) {
            console.error("Failed to unfollow", err);
        }
    };

    const searchSpecific = async (name) => {
        if (!name.trim()) {
            setSearch(null);
            return;
        }

        try {
            const res = await httpClient.get("http://localhost:5000/getStreamer", {
                params: { name }
            });
            setSearch(res.data.streamer);
        } catch (error) {
            console.error("Error fetching streamer:", error);
            setSearch(null);
        }
    };

    return (
        <div>
            <NavBar />

            <div className="search-specific">
                <h2>Don't see a streamer? Search for a specific one:</h2>

                <input
                    type="text"
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    placeholder="Search unfeatured streamer"
                />
                <button type="submit" onClick={() => searchSpecific(searchInput)}>Submit</button>

                <div className="specific-streamer">
                    {search && (
                        <div className="grid-item">
                            <StreamerCard streamer={search}/>
                            {followedID.includes(search.id) ? (
                                <button onClick={() => unfav(search)}>Unsub</button>
                            ) : (
                                <button onClick={() => fav(search)}>Sub</button>
                            )}
                        </div>
                    )}
                </div>

            </div>

            <div className="main-content">

                <div className="featured-bar">
                    <h1>Featured Streamers <span>Showing 50</span></h1>
                </div>
                <div className="featured-search">
                    <input
                        type="text"
                        value={searchFav}
                        onChange={(e) => setSearchFav(e.target.value)}
                        placeholder="Search streamers..."
                    />
                </div>

                <div className="grid-container">
                    {(searchFav
                            ? streamers.filter((streamer) =>
                                streamer.name.toLowerCase().startsWith(searchFav.toLowerCase())
                            )
                            : streamers
                    ).map((streamer) => {
                        const isFav = followedID.includes(streamer.id);
                        return (
                            <div className="grid-item" key={streamer.id}>
                                <StreamerCard streamer={streamer}/>
                                {isFav ? (
                                    <button onClick={() => unfav(streamer)}>Unsub</button>
                                ) : (
                                    <button onClick={() => fav(streamer)}>Sub</button>
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;