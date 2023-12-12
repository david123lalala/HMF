import argparse


def parameter_parser():
    # Experiment parameters
    parser = argparse.ArgumentParser(description='Smart Contracts Reentrancy Detection')

    # parser.add_argument('-D', '--dataset', type=str, default='train_data/reentrancy_1671.txt',
    #                     choices=['train_data/infinite_loop_1317.txt', 'train_data/reentrancy_1671.txt',
    #                              'train_data/timestamp.txt','train_data/reentrancy_code_snippets_2000.txt'])
    parser.add_argument('-D', '--dataset',type=str,default='reentrancy',choices=['reentrancy','train_data/timestamp.txt',])
    parser.add_argument('-M', '--model', type=str, default='transformer_cnn',
                        choices=['transformer_cnn'])
                        
    parser.add_argument('--lr', type=float, default=0.002, help='learning rate')
    parser.add_argument('-d', '--dropout', type=float, default=0.5, help='dropout rate')
    # parser.add_argument('--vector_dim', type=int, default=300, help='dimensions of vector')
    parser.add_argument('--epochs', type=int, default=10, help='number of epochs')
    parser.add_argument('-b', '--batch_size', type=int, default=64, choices=['16','32','64','128'],help='batch size')
    parser.add_argument('-th', '--threshold', type=float, default=0.5, help='threshold')
    parser.add_argument('-k','--kernel_size', type=int, default=2, help='kernel size')
    parser.add_argument('-n','--kernel_num', type=int, default=6, help='filters')

    return parser.parse_args()
