import express from 'express';
import cors from 'cors';
const router = express.Router();
router.use(cors())
import {
    addValidTransaction,
    getOracleData, getValidTransactions, updateOracleData
} from "./controller";

// Add a txn
router.route('/add-transaction').post(addValidTransaction);

// Get all txns
router.route('/valid-transactions').get(getValidTransactions);

// execute
router.route('/oracle-data').post(updateOracleData);

// queries
router.route('/oracle-data').get(getOracleData);

export default router;