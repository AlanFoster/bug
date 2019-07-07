use crate::rocket;
use rocket::local::Client;
use rocket::http::{Status, ContentType};


#[test]
fn post_valid_webassembly_text() {
    let client = Client::new(rocket()).unwrap();

    let mut res =
        client
            .post("/compile")
            .header(ContentType::JSON)
            .body(r#"{ "wast": "(module)" }"#)
            .dispatch();

    assert_eq!(res.status(), Status::Ok);

    let body = res.body_string().unwrap();
    assert!(body.contains("asm"));
}

#[test]
fn post_invalid_webassembly_text() {
    let client = Client::new(rocket()).unwrap();

    let mut res =
        client
            .post("/compile")
            .header(ContentType::JSON)
            .body(r#"{ "wast": "()" }"#)
            .dispatch();

    assert_eq!(res.status(), Status::Ok);

    let body = res.body_string().unwrap();
    assert!(body.contains("failed to parse"));
}
