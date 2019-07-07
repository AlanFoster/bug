#![feature(proc_macro_hygiene, decl_macro)]

use rocket_contrib::json::Json;
use wabt::wat2wasm;
use std::error::Error;

#[macro_use] extern crate rocket;
#[macro_use] extern crate serde_derive;

#[cfg(test)] mod tests;

#[derive(Deserialize)]
struct Request {
    wast: String
}

#[derive(Serialize)]
struct Response {
    result: String
}

#[get("/health")]
fn health() -> &'static str {
    "OK"
}

#[post("/compile", format = "application/json", data = "<request>")]
fn compile(request: Json<Request>) -> Json<Response> {
    match wat2wasm(request.wast.to_string()) {
        Ok(v) => Json(Response { result:  String::from_utf8(v).unwrap() }),
        Err(e) => Json(Response { result: e.description().to_string() })
    }
}


fn rocket() -> rocket::Rocket {
    rocket::ignite()
        .mount("/", routes![health, compile])
}

fn main() {
    rocket().launch();
}
