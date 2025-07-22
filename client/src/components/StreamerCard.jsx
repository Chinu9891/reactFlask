import "./streamerCard.css"

function StreamerCard({streamer}){

    return <div>
        <div>
            <img src={streamer.img} alt={streamer.name} className="streamer-img"/>
        </div>
        <div>
            <h3>{streamer.name}</h3>
        </div>
    </div>

}

export default StreamerCard