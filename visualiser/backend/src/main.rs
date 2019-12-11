#![feature(proc_macro_hygiene, decl_macro)]

use rocket_contrib::json::Json;
use wabt::wat2wasm;
use std::error::Error;
use rocket::fairing::AdHoc;
use rocket::http::{Header, Method, Status};
use rocket::response::status;

#[macro_use]
extern crate rocket;
#[macro_use]
extern crate serde_derive;

#[cfg(test)]
mod tests;

#[derive(Deserialize)]
struct Request {
    wast: String
}

#[derive(Serialize, Debug)]
struct SuccessResponse {
    result: String
}

#[derive(Serialize, Debug)]
struct ErrorResponse {
    error: String
}

#[get("/health")]
fn health() -> &'static str {
    "OK"
}

#[post("/compile", format = "application/json", data = "<request>")]
fn compile(request: Json<Request>) -> Result<status::Accepted<Json<SuccessResponse>>, status::Custom<Json<ErrorResponse>>> {
    match wat2wasm(request.wast.to_string()) {
        Ok(v) => Ok(status::Accepted(Some(Json(SuccessResponse { result: String::from_utf8(v).unwrap() })))),
        Err(e) => Err(status::Custom(Status::BadRequest, Json(ErrorResponse { error: e.description().to_string() })))
    }
}

fn rocket() -> rocket::Rocket {
    rocket::ignite()
        .attach(AdHoc::on_response("CORS", |req, resp| {
            resp.set_header(Header::new(
                "Access-Control-Allow-Origin",
                "*",
            ));
            resp.set_header(Header::new(
                "Access-Control-Allow-Methods",
                "DELETE, GET, HEAD, PATCH, POST, PUT, OPTIONS",
            ));
            resp.set_header(Header::new(
                "Access-Control-Allow-Headers",
                "Authorization, Content-Type",
            ));

            if req.method() == Method::Options {
                resp.set_status(Status::Ok);
            }
        }))
        .mount("/", routes![health, compile])
}

fn main() {
    rocket().launch();
}
