#include "chainparams.h"
#include "consensus/merkle.h"

#include "tinyformat.h"
#include "util.h"
#include "utilstrencodings.h"

#include "arith_uint256.h"
#include "pow.h"

#include <stdio.h>

static CBlock CreateGenesisBlock(const char* pszTimestamp, const CScript& genesisOutputScript, uint32_t nTime, uint32_t nNonce, uint32_t nBits, int32_t nVersion, const CAmount& genesisReward)
{
    CMutableTransaction txNew;
    txNew.nVersion = 1;
    txNew.vin.resize(1);
    txNew.vout.resize(1);
    txNew.vin[0].scriptSig = CScript() << 486604799 << CScriptNum(4) << std::vector<unsigned char>((const unsigned char*)pszTimestamp, (const unsigned char*)pszTimestamp + strlen(pszTimestamp));
    txNew.vout[0].nValue = genesisReward;
    txNew.vout[0].scriptPubKey = genesisOutputScript;

    CBlock genesis;
    genesis.nTime    = nTime;
    genesis.nBits    = nBits;
    genesis.nNonce   = nNonce;
    genesis.nVersion = nVersion;
    genesis.vtx.push_back(MakeTransactionRef(std::move(txNew)));
    genesis.hashPrevBlock.SetNull();
    genesis.hashMerkleRoot = BlockMerkleRoot(genesis);
    return genesis;
}

int main(int argc, char* argv[])
{
  ParseParameters(argc, argv);

  try
  {
    ReadConfigFile(GetArg("-conf", "generate_altcoin.conf"));
  } catch (const std::exception& e) {
    fprintf(stderr,"Error reading configuration file: %s\n", e.what());
    return false;
  }

  std::string powLimit = GetArg("-cp_main_powlimit", "00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff");
  std::string pszTimestamp = GetArg("-cp_main_genesis_block_psz_timestamp", "hi");
  uint32_t nTime = GetArg("-cp_main_genesis_block_ntime", 1000);
  std::string genesisBlockPubKey = GetArg("-cp_main_genesis_block_pubkey", "");
  int32_t nVersion = GetArg("-cp_main_genesis_block_version", 1);
  uint32_t genesisReward = GetArg("-cp_main_genesis_block_reward", 50);
  // CAmount amountGenesisReward = genesisReward * COIN;
  uint32_t nNonce = GetArg("-cp_main_genesis_block_nnonce", 0);

  CBlock genesis;
  Consensus::Params consensus;

  consensus.nSubsidyHalvingInterval = 840000;
  consensus.powLimit = uint256S(powLimit); 
  consensus.nPowTargetTimespan = 3.5 * 24 * 60 * 60; // 3.5 days
  consensus.nPowTargetSpacing = 2.5 * 60;
  consensus.fPowAllowMinDifficultyBlocks = false;
  consensus.fPowNoRetargeting = false;
  consensus.nRuleChangeActivationThreshold = 6048; // 75% of 8064
  consensus.nMinerConfirmationWindow = 8064; // nPowTargetTimespan / nPowTargetSpacing * 4

  // CMessageHeader::MessageStartChars pchMessageStart;
  // pchMessageStart[0] = strtol(GetArg("-cp_main_pch_message_start_0", "0x10").c_str(), NULL, 16);
  // pchMessageStart[1] = strtol(GetArg("-cp_main_pch_message_start_1", "0x10").c_str(), NULL, 16);
  // pchMessageStart[2] = strtol(GetArg("-cp_main_pch_message_start_2", "0x10").c_str(), NULL, 16);
  // pchMessageStart[3] = strtol(GetArg("-cp_main_pch_message_start_3", "0x10").c_str(), NULL, 16);

  const CScript genesisOutputScript = CScript() << ParseHex(genesisBlockPubKey) << OP_CHECKSIG;
  uint32_t nBits = GetNextWorkRequired(nullptr, &genesis, consensus);
  genesis = CreateGenesisBlock(pszTimestamp.c_str(), genesisOutputScript, nTime,
                               nNonce, nBits, nVersion, genesisReward);

  fprintf(stdout, "calculating genesis block.\n");
  fprintf(stdout, "old mainnet genesis nonce: %u\n", genesis.nNonce);
  fprintf(stdout, "old mainnet genesis nBits: %u\n", genesis.nBits);
  fprintf(stdout, "old mainnet genesis merkle root: %s\n", genesis.hashMerkleRoot.ToString().c_str());
  fprintf(stdout, "old mainnet genesis hash:  %s\n", genesis.GetHash().ToString().c_str());
  // deliberately empty for loop finds nonce value.
  genesis.nNonce = 0;
  while (true) {
    if (CheckProofOfWork(genesis.GetPoWHash(), genesis.nBits, consensus)) {
      break;
    }
    genesis.nNonce += 1;
    if (genesis.nNonce == 0) {
      break;
    }
  }
  fprintf(stdout, "new mainnet genesis nonce: %u\n", genesis.nNonce);
  fprintf(stdout, "new mainnet genesis nBits: %u\n", genesis.nBits);
  fprintf(stdout, "new mainnet genesis merkle root: %s\n", genesis.hashMerkleRoot.ToString().c_str());
  fprintf(stdout, "new mainnet genesis hash: %s\n", genesis.GetHash().ToString().c_str());
}
