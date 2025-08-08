import { createPortal } from "react-dom";
import LoginModal from "./LoginModal.jsx";
import {useAtom} from "jotai";
import uiAtom from "./state.jsx";

const targetElement = document.getElementById("popups")

const Overlays = () => {
    const [ui] = useAtom(uiAtom);

    return createPortal(<>{ui.modal && ui.currModal}</>, targetElement)
}

export default Overlays;