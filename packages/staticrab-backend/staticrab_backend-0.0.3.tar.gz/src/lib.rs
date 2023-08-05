//#![deny(rust_2018_idioms)]
use ndarray::{ArrayD, ArrayViewD, ArrayViewMutD};
use numpy::{IntoPyArray, PyArrayDyn};
use pyo3::prelude::{pymodule, Py, PyModule, PyResult, Python};
use staticrab_rust;

#[pymodule]
fn staticrab_backend(_py: Python<'_>, m: &PyModule) -> PyResult<()> {

    #[pyfn(m, "chatterjee_single")]
    fn chatterjee_single_py(
        py: Python<'_>,
        x: &PyArrayDyn<f64>,
        y: &PyArrayDyn<f64>,
        parallel_sort: bool,
        no_checks: bool,
    ) -> PyResult<f64> {
        let x: Vec<f64> = x.as_array().into_iter().cloned().collect();
        let y: Vec<f64> = y.as_array().into_iter().cloned().collect();
        //let y = y.as_array();
        let corr = py.allow_threads(move || staticrab_rust::chatterjee(x, &y, parallel_sort, no_checks));
        Ok(corr)
    }

    #[pyfn(m, "chatterjee_shuffled")]
    fn chatterjee_shuffled_py(
        py: Python<'_>,
        x: &PyArrayDyn<f64>,
        y: &PyArrayDyn<f64>,
        parallel_sort: bool,
        no_checks: bool,
    ) -> PyResult<f64> {
        let x: Vec<f64> = x.as_array().into_iter().cloned().collect();
        let y: Vec<f64> = y.as_array().into_iter().cloned().collect();
        //let y = y.as_array();
        let corr = py.allow_threads(move || staticrab_rust::chatterjee_shuffled(&x, &y, parallel_sort, no_checks));
        Ok(corr)
    }

    #[pyfn(m, "chatterjee_repeated")]
    fn chatterjee_repeated_py(
        py: Python<'_>,
        x: &PyArrayDyn<f64>,
        y: &PyArrayDyn<f64>,
        n_repetitions: i32,
        parallel_runs: bool,
        no_checks: bool,
    ) -> PyResult<f64> {
        let x: Vec<f64> = x.as_array().into_iter().cloned().collect();
        let y: Vec<f64> = y.as_array().into_iter().cloned().collect();
        //let y = y.as_array();
        let corr = py.allow_threads(move || staticrab_rust::chatterjee_repeated(&x, &y, n_repetitions, parallel_runs, no_checks)).iter().sum::<f64>() as f64 / n_repetitions as f64;
        Ok(corr)
    }
    Ok(())
}
