use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

fn main() {
    let x = whamo();
    println!("{:?}", x);
    // let x = go();
    // match x {
    //     Ok(y) => {
    // println!("{:?}", y);
    // println!("what");
    //     }
    //     Err(e) => {
    //         println!("{:?}",e);
    //     }
    // }
}
use pyo3::types::PyTuple;
fn whamo() -> PyResult<i32> {
    let py_foo = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/psbt_faker/delete.py"));
    let py_te = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/psbt_faker/txn.py"));

    let from_python = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
    // Python::with_gil(|py| -> PyResult<Py<PyAny>> {
        let sys = py.import_bound("sys")?;
        let path = sys.getattr("path")?;
        path.call_method1("append", (".venv/lib/python3.7/site-packages",))?;
        path.call_method1("append", ("./",))?;
        path.call_method1("append", ("./psbt_faker",))?;

        let app: Py<PyAny> = PyModule::from_code_bound(py, py_te, "", "")?
            .getattr("fake_txn")?
            .into();
        // let app: Py<PyAny> = PyModule::from_code(py, py_foo, "", "")?
        //     .getattr("what")?
        //     .into();
        // let args = PyTuple::new(py, &[12, 12]);
        let args = (12, 12);
        Ok(app.call1(py, args)?)
        // Ok(what)
        // app.call0(py)?
    });
    println!("py: {}", from_python.unwrap());
    Ok(1)
}

// fn go() -> PyResult<i32> {
//     let mm = Python::with_gil(|py| {
//         let sys = py.import_bound("sys")?;
//         let version: String = sys.getattr("version")?.extract()?;

//         let locals = [
//             ("os", py.import_bound("os")?),
//             ("psbt_faker", py.import_bound("psbt_faker")?),
//         ]
//         .into_py_dict_bound(py);
//         let code = "os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'";
//         let user: String = py.eval_bound(code, None, Some(&locals))?.extract()?;
//         // let psbt: String = py.eval_bound("dir(os)", None, Some(&locals))?.extract()?;

//         let calc: i32 = py.eval_bound("1 + 1", None, None)?.extract().unwrap();

//         // println!("{:?}", psbt);

//         println!("Hello {}, I'm Python {}", user, version);
//         Ok(calc)
//     });
//     mm
// }
