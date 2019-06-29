import {RefObject, useEffect, useState} from 'react';


let count = 0;

export const useHorizontalDrag = function (ref?: RefObject<Element>, initialWidth?: number) {
    const [width, setWidth] = useState(initialWidth);
    const [isDragging, setDragging] = useState(false);

    useEffect(function () {
        if (!ref.current) return;

        const element = ref.current;
        const mouseMovelistener = function (e) {
            const boundingRect = element.getBoundingClientRect();
            setWidth(
                e.clientX - boundingRect.left
            )
        };

        const mouseUpListener = function () {
            setDragging(false)
        };

        if (isDragging) {
            element.addEventListener('mousemove', mouseMovelistener);
            element.addEventListener('mouseup', mouseUpListener)
        }
        return () => {
            element.removeEventListener('mousemove', mouseMovelistener);
            element.removeEventListener('mouseup', mouseUpListener)
        }
    }, [ref, isDragging]);

    return { width, setDragging };
};
