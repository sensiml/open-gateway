export class BaseStreamHttpError extends Error {
  constructor(errorCode, response) {
    super();
    if (errorCode !== 500) {
      this.detail = response.detail;
    } else {
      this.detail = 'Server Error. Please, contact support.';
    }
    this.name = this.constructor.name;
    this.errorCode = errorCode;
  }
}