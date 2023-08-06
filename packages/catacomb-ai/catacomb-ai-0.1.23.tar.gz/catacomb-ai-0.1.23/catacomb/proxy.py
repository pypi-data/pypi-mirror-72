import asyncio
import websockets
import json


def connect(system, input_type="TEXT", output_type="TEXT"):
    asyncio.get_event_loop().run_until_complete(proxy(system, input_type, output_type))


async def proxy(system, input_type, output_type):
    uri = "wss://beta.catacomb.ai/ws/proxy/"
    async with websockets.connect(uri) as websocket:
        model_id = ""
        await websocket.send(json.dumps({
            "type": "types",
            "input_type": input_type,
            "output_type": output_type,
        }))
        while True:
            text_data = await websocket.recv()
            data = json.loads(text_data)
            if data["type"] == "connect":
                model_id = data["id"]
                print(f"Started at https://beta.catacomb.ai/api/predict_proxy/{model_id}/")
            elif data["type"] == "request":
                req = data["request"]["input"]
                req_id = data["req_id"]
                output = system.output(req)
                await websocket.send(json.dumps({
                    "type": "response",
                    "response": output,
                    "req_id": req_id,
                }))
