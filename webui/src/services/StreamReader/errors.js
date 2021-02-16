export class BaseStreamHttpError extends Error {
  constructor(errorCode, response) {
    super();
    if (errorCode !== 500) {
      this.message = response.message;
    } else {
      this.message = 'Server Error. Please, contact support.';
    }
    this.name = this.constructor.name;
    this.errorCode = errorCode;
  }
}