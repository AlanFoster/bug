import axios from 'axios';

interface ServerResponse {
    result: string
}

export const compileText = async function (text: string): Promise<ArrayBuffer> {
    const response = await axios.post<ServerResponse>('http://localhost:8000/compile', {
        wast: text
    });
    const wasmString = response.data.result;

    return new TextEncoder().encode(wasmString).buffer;
};
